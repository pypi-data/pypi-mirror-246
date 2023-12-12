import abc
from typing import Any, AsyncIterator, Dict, List, Tuple

from dap.conversion_perf import create_copy_converters, create_upsert_converters, disabled_create_copy_converters
from dap.dap_types import VersionedSchema
from dap.integration.base_processor import JSONLRecordProcessor, JsonRecord, TsvRecord, TSVRecordProcessor
from dap.integration.connection import AbstractQueryExecutor
from dap.integration.processor import ContextAwareObject
from dap.plugins.sqlalchemy.queries import SqlAlchemyExecutableQuery, SqlAlchemySyncQuery
from dap.timer import Timer
from sqlalchemy import BindParameter, Connection, Inspector, Table, bindparam, inspect
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema
from sqlalchemy.sql.dml import Insert

from .metadata import create_table_definition
from .queries import AsyncpgQuery


def _create_tables(conn: Connection, table_def: Table) -> None:
    inspector: Inspector = inspect(conn)

    if table_def.schema is not None and not inspector.has_schema(table_def.schema):
        conn.execute(CreateSchema(table_def.schema))  # type: ignore

    table_def.metadata.create_all(conn)

class PostgresInsert:
    "Base class for insert logic."

    @abc.abstractmethod
    async def insert(self, db_connection: AbstractQueryExecutor[AsyncConnection], table_def: Table, records: AsyncIterator[JsonRecord]) -> None:
        "Insert data into table."

class CopyInsert(PostgresInsert):
    "Copy statement."
    async def _convert_records(
        self, records: AsyncIterator[JsonRecord], table_def: Table
    ) -> AsyncIterator[Tuple]:
        async for record in records:
            yield tuple(converter(record) for converter in create_copy_converters(table_def))

    async def insert(self, db_connection: AbstractQueryExecutor[AsyncConnection], table_def: Table, records: AsyncIterator[JsonRecord]) -> None:
        await db_connection.execute(
            AsyncpgQuery[None](
                lambda connection: connection.copy_records_to_table(  # type: ignore
                    schema_name=table_def.metadata.schema,
                    table_name=table_def.name,
                    columns=[col.name for col in table_def.columns],
                    records=self._convert_records(records, table_def),
                )
            )
        )

class InsertOnConflictDoNothing(PostgresInsert):
    "Accounts for potential duplicate PK by throwing it away."

    async def _convert_records(
        self, records: AsyncIterator[JsonRecord], table_def: Table
    ) -> List[Dict[str, Any]]:
        converted_records: List[Dict[str, Any]] = list()
        async for record in records:
            sql_item = {
                col_name: converter(record)
                for col_name, converter in create_upsert_converters(table_def).items()
            }
            converted_records.append(sql_item)
        return converted_records

    async def insert(self, db_connection: AbstractQueryExecutor[AsyncConnection], table_def: Table, records: AsyncIterator[JsonRecord]) -> None:
        values_clause: Dict[str, BindParameter] = {}
        for col in table_def.columns:
            values_clause[col.name] = bindparam(col.name)
        upsert_statement: Insert = (
            insert(table_def)
            .values(values_clause)
            .on_conflict_do_nothing()
        )

        converted_records = await self._convert_records(records, table_def)
        await db_connection.execute(
            SqlAlchemyExecutableQuery[None](
                upsert_statement, converted_records
            )
        )

class PostgresInsertFactory:
    @staticmethod
    def create(table_def: Table) -> PostgresInsert:
        if table_def.name == "web_logs":
            return InsertOnConflictDoNothing()
        else:
            return CopyInsert()

class InitProcessor(JSONLRecordProcessor):
    """
    Creates and populates an empty database table with records acquired from the DAP service.
    """

    _db_connection: AbstractQueryExecutor[AsyncConnection]
    _table_def: Table
    _converters: Tuple

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, table_schema)

    async def prepare(self) -> None:
        await self._db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: _create_tables(connection, self._table_def)
            )
        )

    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[JsonRecord]
    ) -> None:
        async with Timer(f"inserting records from {obj}"):
            insert_statement = PostgresInsertFactory.create(self._table_def)
            await insert_statement.insert(self._db_connection, self._table_def, records)

    async def close(self) -> None:
        pass


# TODO: this class is to be used when full TSV support is enabled on the backend.
class DisabledInitProcessor(TSVRecordProcessor):
    """
    Creates and populates an empty database table with records acquired from the DAP service.
    """

    _db_connection: AbstractQueryExecutor[AsyncConnection]
    _table_def: Table
    _converters: Tuple

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        self._db_connection = db_connection
        self._table_def = create_table_definition(namespace, table_name, table_schema)
        self._converters = disabled_create_copy_converters(self._table_def)

        super().__init__(
            all_columns=[col.name for col in self._table_def.columns],
            primary_key_columns=[col.name for col in self._table_def.primary_key],
        )

    async def prepare(self) -> None:
        await self._db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: _create_tables(connection, self._table_def)
            )
        )

    async def process_impl(
        self, obj: ContextAwareObject, records: AsyncIterator[TsvRecord]
    ) -> None:
        async with Timer(f"inserting records from {obj}"):
            await self._db_connection.execute(
                AsyncpgQuery[None](
                    lambda connection: connection.copy_records_to_table(  # type: ignore
                        schema_name=self._table_def.metadata.schema,
                        table_name=self._table_def.name,
                        columns=[col.name for col in self._table_def.columns],
                        records=self._convert_records(records),
                    )
                )
            )

    async def close(self) -> None:
        pass

    async def _convert_records(
        self, records: AsyncIterator[TsvRecord]
    ) -> AsyncIterator[Tuple]:
        async for record in records:
            yield tuple(converter(record) for converter in self._converters)
