import logging
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from shutil import rmtree
from typing import AsyncContextManager, Awaitable, Callable, Iterator, Optional

from .api import DAPSession, DownloadError
from .concurrency import wait_n
from .dap_types import (
    Format,
    GetTableDataResult,
    IncrementalQuery,
    Object,
    SnapshotQuery,
    TableQuery,
    VersionedSchema,
)
from .integration.database_errors import SchemaVersionMismatchError
from .integration.processor import AbstractProcessor, ContextAwareObject
from .payload import get_lines_from_gzip_file

logger = logging.getLogger("dap")

CONCURRENCY: int = 4
DEFAULT_FOLDER: str = "instructure_dap_temp"

DatabaseLock = Callable[[], AsyncContextManager]
Downloader = Callable[[DatabaseLock, AbstractProcessor], Awaitable[None]]


@contextmanager
def use_and_remove(directory: str) -> Iterator[str]:
    """Remove a directory after use."""

    try:
        yield directory
    finally:
        rmtree(directory)
        logger.info(f"Removed folder: {directory}")


@dataclass(frozen=True)
class SnapshotClient:
    table_data: GetTableDataResult
    table_schema: VersionedSchema
    download: Downloader


class _BaseClient:
    @staticmethod
    async def load_file_to_db(
        db_lock: DatabaseLock,
        obj: ContextAwareObject,
        file_path: str,
        processor: AbstractProcessor,
    ) -> None:
        """Save a local file to db."""

        if not file_path:
            raise DownloadError("Unable to download the resource URL")

        records = get_lines_from_gzip_file(file_path)
        async with db_lock():
            await processor.process(obj, records)


class SnapshotClientFactory(_BaseClient):
    _sessions: DAPSession
    _namespace: str
    _table: str
    _query: SnapshotQuery

    def __init__(
        self,
        session: DAPSession,
        namespace: str,
        table: str,
        query: Optional[TableQuery] = None,
    ) -> None:
        if query is None:
            query = TableQuery(format=Format.JSONL, mode=None, filter=None)

        self._session = session
        self._namespace = namespace
        self._table = table
        self._query = SnapshotQuery(format=query.format, mode=None, filter=query.filter)

    async def get_client(self) -> SnapshotClient:
        table_data = await self._session.get_table_data(
            self._namespace, self._table, self._query
        )

        table_schema = await self._session.get_table_schema(
            self._namespace, self._table
        )
        if table_schema.version != table_data.schema_version:
            raise SchemaVersionMismatchError(
                table_schema.version, table_data.schema_version
            )

        object_count = len(table_data.objects)
        job_id = table_data.job_id

        async def download(db_lock: DatabaseLock, processor: AbstractProcessor) -> None:
            resources = await self._session.get_resources(table_data.objects)

            with use_and_remove(DEFAULT_FOLDER) as directory:
                file_paths = await self._session.download_resources(
                    list(resources.values()), directory
                )

                async def save(obj: Object, index: int) -> None:
                    context_aware_object = ContextAwareObject(
                        id=obj.id,
                        index=index,
                        job_id=job_id,
                        total_count=object_count,
                    )
                    await self.load_file_to_db(
                        db_lock,
                        context_aware_object,
                        file_paths[index],
                        processor=processor,
                    )

                await wait_n(
                    [
                        save(obj, obj_index)
                        for obj_index, obj in enumerate(table_data.objects)
                    ],
                    concurrency=CONCURRENCY,
                )

                await processor.close()

        return SnapshotClient(
            table_schema=table_schema, table_data=table_data, download=download
        )


@dataclass(frozen=True)
class IncrementalClient:
    table_data: GetTableDataResult
    table_schema: VersionedSchema
    download: Downloader


class IncrementalClientFactory(_BaseClient):
    _session: DAPSession
    _namespace: str
    _table: str
    _query: IncrementalQuery

    def __init__(
        self,
        session: DAPSession,
        namespace: str,
        table: str,
        since: datetime,
        query: Optional[TableQuery] = None,
    ) -> None:
        if query is None:
            query = TableQuery(format=Format.JSONL, mode=None, filter=None)

        self._session = session
        self._namespace = namespace
        self._table = table
        self._query = IncrementalQuery(
            format=query.format, mode=None, filter=query.filter, since=since, until=None
        )

    async def get_client(self) -> IncrementalClient:
        table_data = await self._session.get_table_data(
            self._namespace, self._table, self._query
        )

        table_schema = await self._session.get_table_schema(
            self._namespace, self._table
        )
        if table_schema.version != table_data.schema_version:
            raise SchemaVersionMismatchError(
                table_schema.version, table_data.schema_version
            )

        job_id = table_data.job_id
        object_count = len(table_data.objects)

        async def download(db_lock: DatabaseLock, processor: AbstractProcessor) -> None:
            resources = await self._session.get_resources(table_data.objects)

            with use_and_remove(DEFAULT_FOLDER) as directory:
                file_paths = await self._session.download_resources(
                    list(resources.values()), directory
                )

                for index, obj in enumerate(table_data.objects):
                    context_aware_object = ContextAwareObject(
                        id=obj.id,
                        index=index,
                        job_id=job_id,
                        total_count=object_count,
                    )
                    await self.load_file_to_db(
                        db_lock, context_aware_object, file_paths[index], processor
                    )

                await processor.close()

        return IncrementalClient(
            download=download, table_data=table_data, table_schema=table_schema
        )
