import abc
import json
import logging
import typing
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar

import sqlalchemy
from sqlalchemy import CursorResult, Row
from sqlalchemy.ext.asyncio import AsyncConnection
from strong_typing.core import JsonType, Schema
from strong_typing.serialization import json_to_object

from ..dap_types import GetTableDataResult, VersionedSchema
from .connection import AbstractQueryExecutor
from .meta_table import AbstractMetaTableManager
from ..plugins.sqlalchemy.queries import SqlAlchemyExecutableQuery, SqlAlchemySyncQuery

TRawConnection = TypeVar("TRawConnection")

logger = logging.getLogger("dap.base_meta_table")


def create_metatable_def(namespace: str) -> sqlalchemy.Table:
    metadata = sqlalchemy.MetaData(schema=namespace)
    metatable = sqlalchemy.Table(
        "dap_meta",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("namespace", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("source_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("timestamp", sqlalchemy.DateTime(), nullable=False),
        sqlalchemy.Column("schema_version", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("target_schema", sqlalchemy.String(64), nullable=True),
        sqlalchemy.Column("target_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column(
            "schema_description_format", sqlalchemy.String(64), nullable=False
        ),
        sqlalchemy.Column("schema_description", sqlalchemy.Text(), nullable=False),
        sqlalchemy.UniqueConstraint(
            "namespace",
            "source_table",
            name="UQ__dap_meta__namespace__source_table",
        ),
    )
    return metatable


class MetatableRecord:
    namespace: str
    table_name: str
    timestamp: datetime
    versioned_schema: VersionedSchema
    metadata: sqlalchemy.MetaData

    @staticmethod
    async def load(
        db_conn: AbstractQueryExecutor[AsyncConnection],
        namespace: str,
        table_name: str,
        metatable_def: sqlalchemy.Table,
    ) -> "MetatableRecord":
        metatable_record: typing.Optional[Row] = (
            await db_conn.execute(
                SqlAlchemyExecutableQuery[CursorResult](
                    metatable_def.select()
                    .where(metatable_def.c.namespace == namespace)
                    .where(metatable_def.c.source_table == table_name)
                    .limit(1)
                )
            )
        ).first()

        if metatable_record is None:
            raise NoMetadataError(namespace, table_name)

        schema_description_format: str = metatable_record._mapping[
            "schema_description_format"
        ]
        if schema_description_format != "json":
            raise WrongSchemaDescriptionError(schema_description_format)

        schema_description: JsonType = json.loads(
            metatable_record._mapping["schema_description"]
        )

        schema_version: int = metatable_record._mapping["schema_version"]
        versioned_schema: VersionedSchema = VersionedSchema(
            typing.cast(Schema, json_to_object(Schema, schema_description)),
            schema_version,
        )

        record = MetatableRecord(
            namespace, table_name, versioned_schema, metatable_def.metadata
        )
        record.timestamp = metatable_record._mapping["timestamp"]
        return record

    def __init__(
        self,
        namespace: str,
        table_name: str,
        versioned_schema: VersionedSchema,
        metadata: sqlalchemy.MetaData,
    ) -> None:
        self.namespace = namespace
        self.table_name = table_name
        self.versioned_schema = versioned_schema
        self.metadata = metadata


class BaseMetaTableManager(AbstractMetaTableManager, Generic[TRawConnection]):
    """
    The abstract base class that implements the AbstractMetaTableManager interface.

    Plugin developers should typically derive from this class.
    """

    _db_connection: AbstractQueryExecutor[TRawConnection]
    _namespace: str
    _table_name: str

    def __init__(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        self._db_connection = db_connection
        self._namespace = namespace
        self._table_name = table_name

    async def get_timestamp(self) -> datetime:
        return await self.get_timestamp_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
        )

    async def initialize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await self.initialize_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
            table_data,
        )

    async def synchronize(
        self,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        await self.update_table_schema_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
        )
        await self.update_table_data_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
        )
        await self.synchronize_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
            table_schema,
            table_data,
        )

    async def drop(self) -> None:
        await self.drop_impl(
            self._db_connection,
            self._namespace,
            self._table_name,
        )

    @abc.abstractmethod
    async def get_timestamp_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> datetime:
        """
        Gets the timestamp (in UTC) of the given source table using the given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :returns: The timestamp in UTC format.
        """
        ...

    @abc.abstractmethod
    async def initialize_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Creates the metatable in the local database (if not yet created) and registers an entry about the given source table using the
        given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The current schema of the source table at the DAP API.
        :param table_data: The result of the DAP API snapshot query of the source table containing the current schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def synchronize_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
        table_data: GetTableDataResult,
    ) -> None:
        """
        Updates the timestamp, schema version and schema description of the given source table entry in the metatable using the
        given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The current schema of the source table at the DAP API.
        :param table_data: The result of the DAP API snapshot query of the source table containing the current schema version and timestamp.
        """
        ...

    @abc.abstractmethod
    async def drop_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
    ) -> None:
        """
        Drops the entry about the given source table from the metatable and drops the corresponding target table as well using the given database connection.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        """
        ...

    @abc.abstractmethod
    async def update_table_schema_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        """
        Updates the schema of the given source table in the local database using the given database connection if the currently
        registered schema version is lower than the given schema version downloaded from the DAP API.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The new schema description downloaded from the DAP API.
        """
        ...

    @abc.abstractmethod
    async def update_table_data_impl(
        self,
        db_connection: AbstractQueryExecutor[TRawConnection],
        namespace: str,
        table_name: str,
        table_schema: VersionedSchema,
    ) -> None:
        """
        Updates the table data of the given source table in the local database using the given database connection if the currently
        registered schema version is lower than the given schema version downloaded from the DAP API.

        :param db_connection: The database connection to be used.
        :param namespace: The namespace of the source table at the DAP API.
        :param table_name: The name of the source table at the DAP API.
        :param table_schema: The new schema description downloaded from the DAP API.
        """
        ...


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


@dataclass
class TableDataUpdater:
    # Contains the table name and schema version of the tables that need to be updated.
    @dataclass
    class CanvasLogsWebLogsV4tov5:
        canvas_logs_namespace = "canvas_logs"
        web_logs_table_name = "web_logs"
        user_agents_table_name = "user_agents"
        schema_version_to_update_from = 4
        schema_version_to_update_to = 5
