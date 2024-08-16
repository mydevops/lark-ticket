"""FastAPI 事件 hook.

启动时创建数据库表.
关闭时回收数据库会话.
"""

from fastapi import FastAPI
from loguru import logger

from src.db import base as db
from src.db.base import Base
from src.db.base import sessionmanager
from src.lib import util


def _register_startup_event(app: FastAPI):
    """注册 FastAPI 应用的启动事件.

    Args:
        app: FastAPI 实例.
    """

    @app.on_event("startup")
    async def _startup() -> None:
        """在应用启动时执行的操作."""
        app.middleware_stack = None
        if util.scheduler_lock() is False:
            # 创建数据库表
            db.init()
            async with sessionmanager.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        app.middleware_stack = app.build_middleware_stack()


def _register_shutdown_event(app: FastAPI):
    """注册 FastAPI 应用的关闭事件.

    Args:
        app: FastAPI 实例.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        """在应用关闭时执行的操作."""
        if sessionmanager.engine is not None:
            # 关闭数据库会话
            await sessionmanager.close()
        logger.remove()


def register(app: FastAPI) -> None:
    """注册 FastAPI 应用的启动和关闭事件.

    Args:
        app: FastAPI 实例.
    """
    _register_startup_event(app)
    _register_shutdown_event(app)
