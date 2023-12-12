import logging
from datetime import datetime, timezone
from typing import Dict, List

import sqlalchemy
from sqlalchemy import (
    Column,
    ColumnDefault,
    Connection,
    Inspector,
    MetaData,
    Table,
    bindparam,
    inspect,
    text,
)
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema
from strong_typing.serialization import json_dump_string

from dap.dap_types import GetTableDataResult, VersionedSchema
from dap.integration.base_meta_table import (
    BaseMetaTableManager,
    TableDataUpdater,
    create_metatable_def,
    MetatableRecord,
)
from dap.integration.connection import AbstractQueryExecutor
from dap.integration.database_errors import NonExistingTableError
from dap.plugins.sqlalchemy.ddl import column_name, table_name, value_literal
from dap.plugins.sqlalchemy.queries import (
    SqlAlchemyExecutableQuery,
    SqlAlchemySyncQuery,
)
from .metadata import create_table_definition

logger = logging.getLogger("dap.mysql.meta_table")


class MysqlMetaTableManager(BaseMetaTableManager[AsyncConnection]):
    _metatable_def: sqlalchemy.Table

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        super().__init__(db_connection, namespace, table_name)
        self._metatable_def = create_metatable_def(namespace)

    async def get_timestamp_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
    ) -> datetime:
        metatable_record = await MetatableRecord.load(
            db_connection, namespace, table_name, self._metatable_def
        )
        return metatable_record.timestamp.replace(tzinfo=timezone.utc)

    async def initialize_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await db_connection.execute(SqlAlchemySyncQuery[None](self._create_tables))
        await db_connection.execute(
            SqlAlchemyExecutableQuery[None](
                self._metatable_def.insert(),
                [
                    {
                        "namespace": namespace,
                        "source_table": table_name,
                        "timestamp": table_data.timestamp.astimezone(
                            tz=timezone.utc
                        ).replace(tzinfo=None),
                        "schema_version": table_data.schema_version,
                        "target_schema": namespace,
                        "target_table": table_name,
                        "schema_description_format": "json",
                        "schema_description": json_dump_string(table_schema.schema),
                    }
                ],
            )
        )

    async def synchronize_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await db_connection.execute(
            SqlAlchemyExecutableQuery[None](
                (
                    self._metatable_def.update()
                    .where(self._metatable_def.c.namespace == namespace)
                    .where(self._metatable_def.c.source_table == table_name)
                    .values(
                        timestamp=bindparam("new_timestamp"),
                        schema_version=bindparam("new_schema_version"),
                        schema_description=bindparam("new_schema_description"),
                    )
                ),
                [
                    {
                        "new_timestamp": table_data.timestamp.astimezone(
                            timezone.utc
                        ).replace(tzinfo=None),
                        "new_schema_version": table_data.schema_version,
                        "new_schema_description": json_dump_string(table_schema.schema),
                    }
                ],
            )
        )

        # In MySQL, enum values are stored as integers, and you can add new values
        # to an existing enum type without committing the change.
        # However, you should be careful when adding new values to an enum type,
        # as it can cause issues with data consistency if the new value is not
        # handled properly in your application.
        await db_connection.commit()

    async def update_table_data_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        await self.update_web_logs_v4_to_v5(
            db_connection,
            namespace,
            table_name,
            table_schema,
        )

    async def update_web_logs_v4_to_v5(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        u_data = TableDataUpdater.CanvasLogsWebLogsV4tov5
        web_logs_table_name = f"{u_data.canvas_logs_namespace}__{u_data.user_agents_table_name}",
        user_agents_table_name = f"{u_data.canvas_logs_namespace}__{u_data.web_logs_table_name}"

        if table_name != web_logs_table_name:
            return
        # if user agents table does not exist, do nothing, return.
        if not await db_connection.execute(
            SqlAlchemySyncQuery[bool](
                lambda connection: connection.dialect.has_table(
                    connection, user_agents_table_name
                )
            )
        ):
            logger.debug(f"Table {user_agents_table_name} does not exist.")
            return

        metatable_record = await MetatableRecord.load(
            db_connection, namespace, table_name, self._metatable_def
        )
        web_logs_table_schema_version = metatable_record.versioned_schema.version

        if (
            table_name == web_logs_table_name
            and web_logs_table_schema_version <= u_data.schema_version_to_update_from
            and table_schema.version >= u_data.schema_version_to_update_to
        ):
            logger.debug(f"Table data should be updated for {web_logs_table_name}.")
            query = f"""
                UPDATE {web_logs_table_name}
                JOIN {user_agents_table_name} ON {web_logs_table_name}.user_agent_id = {user_agents_table_name}.id
                SET {web_logs_table_name}.user_agent = {user_agents_table_name}.http_user_agent
                WHERE {web_logs_table_name}.user_agent_id IS NOT NULL;
            """,
            logger.info(
                f"To migrate the data from the {web_logs_table_name} table schema version {web_logs_table_schema_version} "
                f"to version {u_data.schema_version_to_update_to}, run the following query: {query}"
            )
        else:
            logger.debug(
                f"No data update {web_logs_table_name}, schema version: {web_logs_table_schema_version}"
            )

    async def update_table_schema_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        metatable_record = await MetatableRecord.load(
            db_connection,
            namespace,
            table_name,
            self._metatable_def,
        )

        previous_dap_schema: VersionedSchema = metatable_record.versioned_schema
        desired_dap_schema: VersionedSchema = table_schema
        if previous_dap_schema.version == desired_dap_schema.version:
            return

        current_table_columns: List[ReflectedColumn] = await db_connection.execute(
            SqlAlchemySyncQuery[List[ReflectedColumn]](self._get_table_columns)
        )

        await self._alter_table(
            db_connection,
            prev_table_def=create_table_definition(
                namespace, table_name, previous_dap_schema
            ),
            desired_table_def=create_table_definition(
                namespace, table_name, desired_dap_schema
            ),
            current_table_cols=current_table_columns,
        )

    def _get_table_columns(self, db_conn: Connection) -> List[ReflectedColumn]:
        inspector: Inspector = inspect(db_conn)
        return inspector.get_columns(self._table_name, self._namespace)

    async def drop_impl(
        self,
        db_connection: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        await db_connection.execute(
            SqlAlchemySyncQuery[None](
                lambda connection: self._drop_table(connection, namespace, table_name)
            )
        )

        await db_connection.execute(
            SqlAlchemyExecutableQuery[None](
                self._metatable_def.delete()
                .where(self._metatable_def.c.namespace == namespace)
                .where(self._metatable_def.c.source_table == table_name)
            )
        )

    @staticmethod
    def _drop_table(db_connection: Connection, namespace: str, table_name: str) -> None:
        inspector: Inspector = inspect(db_connection)
        if not inspector.has_table(table_name=table_name, schema=namespace):
            raise NonExistingTableError(namespace, table_name)

        table_def = Table(table_name, MetaData(schema=namespace))
        table_def.drop(bind=db_connection)

    def _create_tables(self, db_conn: Connection) -> None:
        inspector: Inspector = inspect(db_conn)
        if self._metatable_def.schema is not None and not inspector.has_schema(
            self._metatable_def.schema
        ):
            db_conn.execute(CreateSchema(self._metatable_def.schema))  # type: ignore

        self._metatable_def.metadata.create_all(db_conn)

    async def _alter_table(
        self,
        db_conn: AbstractQueryExecutor[AsyncConnection],
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        await self._drop_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )
        await self._add_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )
        await self._alter_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )

    @staticmethod
    async def _drop_columns(
        db_conn: AbstractQueryExecutor[AsyncConnection],
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols: Dict[str, ReflectedColumn] = {
            col["name"]: col for col in current_table_cols
        }
        desired_cols: Dict[str, Column] = {
            col.name: col for col in desired_table_def.columns
        }

        for col_name in current_cols:
            if desired_cols.get(col_name) is None:
                await db_conn.execute(
                    SqlAlchemyExecutableQuery[None](
                        text(
                            f"""
                            ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                            DROP COLUMN {column_name(col_name)}
                            """
                        )
                    )
                )

    @staticmethod
    async def _add_columns(
        db_conn: AbstractQueryExecutor[AsyncConnection],
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols: Dict[str, ReflectedColumn] = {
            col["name"]: col for col in current_table_cols
        }
        desired_cols: Dict[str, Column] = {
            col.name: col for col in desired_table_def.columns
        }

        for col_name in desired_cols:
            if current_cols.get(col_name) is None:
                col_def: Column = desired_cols[col_name]

                column_default: ColumnDefault
                if col_def.nullable and not col_def.default:
                    await db_conn.execute(
                        SqlAlchemyExecutableQuery[None](
                            lambda conn: text(
                                f"""
                                ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                                ADD COLUMN {column_name(col_name)} {col_def.type.compile(conn.dialect)}
                                """
                            )
                        )
                    )
                elif (
                    col_def.nullable
                    and col_def.default
                    and isinstance(col_def.default, ColumnDefault)
                ):
                    column_default = col_def.default
                    await db_conn.execute(
                        SqlAlchemyExecutableQuery[None](
                            lambda conn: text(
                                f"""
                                ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                                ADD COLUMN {column_name(col_name)} {col_def.type.compile(conn.dialect)}
                                DEFAULT {value_literal(column_default.arg)}
                                """
                            )
                        )
                    )
                elif not col_def.nullable and not col_def.default:
                    await db_conn.execute(
                        SqlAlchemyExecutableQuery[None](
                            lambda conn: text(
                                f"""
                                ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                                ADD COLUMN {column_name(col_name)} {col_def.type.compile(conn.dialect)} NOT NULL
                                """
                            )
                        )
                    )
                elif (
                    not col_def.nullable
                    and col_def.default
                    and isinstance(col_def.default, ColumnDefault)
                ):
                    column_default = col_def.default
                    await db_conn.execute(
                        SqlAlchemyExecutableQuery[None](
                            lambda conn: text(
                                f"""
                                ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                                ADD COLUMN {column_name(col_name)} {col_def.type.compile(conn.dialect)} NOT NULL
                                DEFAULT {value_literal(column_default.arg)}
                                """,
                            )
                        )
                    )

    async def _alter_columns(
        self,
        db_conn: AbstractQueryExecutor[AsyncConnection],
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols = {col["name"]: col for col in current_table_cols}
        desired_cols = {col.name: col for col in desired_table_def.columns}

        altered_cols = {
            col_name: desired_cols[col_name]
            for col_name in (set(desired_cols).intersection(set(current_cols)))
        }

        for col_name, col_def in altered_cols.items():
            await self._alter_type(db_conn, col_def, desired_table_def)

    @staticmethod
    async def _alter_type(
        db_conn: AbstractQueryExecutor[AsyncConnection],
        col_def: Column,
        desired_table_def: Table,
    ) -> None:
        col_type = type(col_def.type)
        if not col_type is sqlalchemy.Enum:
            # Only dealing with enum types
            return

        enum_type_def: sqlalchemy.Enum = col_def.type  # type: ignore
        if not enum_type_def.name:
            # Only dealing with named enum types
            return

        await db_conn.execute(
            SqlAlchemyExecutableQuery[None](
                text(
                    f"""
                    ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                    MODIFY COLUMN {col_def.name}
                    enum({', '.join([value_literal(value) for value in enum_type_def.enums])})
                    """,
                )
            )
        )


class MetadataError(Exception):
    """
    Generic base class for specific meta-table related errors.
    """


class NoMetadataError(MetadataError):
    def __init__(self, namespace: str, table_name: str) -> None:
        super().__init__(
            f"metadata not found for table `{table_name}` in `{namespace}`"
        )


class WrongSchemaDescriptionError(MetadataError):
    def __init__(self, schema_description_format: str) -> None:
        super().__init__(
            f"wrong schema description format; expected: json, got: {schema_description_format}"
        )
