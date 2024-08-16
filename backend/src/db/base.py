"""数据库会话、基类模块."""

import contextlib
import importlib
import os
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.schema import CreateTable

from src.lib import const
from src.lib.config import settings


def init():
    """动态加载所有表."""
    for table in os.listdir(os.path.dirname(__file__)):
        if table.endswith(const.BASIC_PYTHON_FILE_SUFFIX) and table not in const.DATABASE_EXCLUDE_FILE:
            table_name = table.split(const.BASIC_PYTHON_FILE_SUFFIX)[0]
            importlib.import_module(f"{const.DATABASE_ROOT}.{table_name}")


class Base(DeclarativeBase):
    """所有表的基类."""

    @classmethod
    def show_create_table_sql(cls) -> CreateTable:
        """生成 CREATE TABLE SQL 语句."""
        return CreateTable(cls.__table__)  # type: ignore


class HasIdMixin:
    """id 字段."""

    id: Mapped[int] = mapped_column(
        primary_key=const.DATABASE_FIELD_ID_PRIMARY_KEY,
        autoincrement=const.DATABASE_FIELD_ID_AUTOINCREMENT,
        sort_order=const.DATABASE_FIELD_ID_SORT_ORDER,
    )


class HasCreateTimeMixin:
    """创建时间字段."""

    create_time: Mapped[datetime] = mapped_column(
        server_default=text(const.DATABASE_FIELD_CREATETIME_SERVER_DEFAULT),
        sort_order=const.DATABASE_FIELD_CREATETIME_SORT_ORDER,
    )


class HasLastUpdateTimeMixin:
    """最后一次更新时间字段."""

    last_update_time: Mapped[datetime] = mapped_column(
        server_default=text(const.DATABASE_FIELD_LASTUPDATETIME_SERVER_DEFAULT),
        sort_order=const.DATABASE_FIELD_LASTUPDATETIME_SORT_ORDER,
    )


class DatabaseSessionManager:
    """会话管理."""

    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None):
        """初始化数据库会话管理器.

        Args:
            host: 数据库连接地址.
            engine_kwargs: 创建引擎时的附加参数.
        """
        if engine_kwargs is None:
            engine_kwargs = {}
        self.engine = create_async_engine(
            host,
            **engine_kwargs,
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=const.DATABASE_SESSION_PARAM_AUTOCOMMIT,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=const.DATABASE_SESSION_PARAM_EXPIRE_ON_COMMIT,
        )

    async def close(self):
        """关闭数据库连接."""
        if self.engine is None:
            raise Exception(const.DATABASE_SESSION_NOT_INITIALIZED_EXCEPTION_PROMPT_MESSAGE)
        await self.engine.dispose()

        self.engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """提供数据库连接上下文管理器."""
        if self.engine is None:
            raise Exception(const.DATABASE_SESSION_NOT_INITIALIZED_EXCEPTION_PROMPT_MESSAGE)

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
            finally:
                await connection.close()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """提供数据库会话上下文管理器."""
        if self._sessionmaker is None:
            raise Exception(const.DATABASE_SESSION_NOT_INITIALIZED_EXCEPTION_PROMPT_MESSAGE)

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    settings.mysql.dsn,
    {
        "echo": settings.basic.debug,
        "pool_size": const.DATABASE_SESSION_PARAM_POOL_SIZE,
        "max_overflow": const.DATABASE_SESSION_PARAM_MAX_OVERFLOW,
        "pool_pre_ping": const.DATABASE_SESSION_PARAM_POOL_PRE_PING,
    },
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """获取数据库会话,配合 FastAPI Depends 使用."""
    async with sessionmanager.session() as session:
        yield session
