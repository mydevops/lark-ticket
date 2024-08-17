"""FastAPI 事件 hook.

启动时创建数据库表.
关闭时回收数据库会话.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.db import base as db
from src.db.base import Base
from src.db.base import sessionmanager
from src.lib import util


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 生命周期."""
    # 在应用启动时执行的操作.
    app.middleware_stack = None
    if util.scheduler_lock() is False:
        # 创建数据库表
        db.init()
        async with sessionmanager.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    app.middleware_stack = app.build_middleware_stack()

    yield

    # 在应用关闭时执行的操作.
    if sessionmanager.engine is not None:
        # 关闭数据库连接
        await sessionmanager.close()
    logger.remove()
