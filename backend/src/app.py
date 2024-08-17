"""初始化 FastAPI 实例."""

from fastapi import FastAPI

from src.api.router import api_router
from src.lib import config
from src.lib import event
from src.lib import extension
from src.lib import middleware


def make_app() -> FastAPI:
    """创建并配置 FastAPI 应用."""
    # 初始化扩展模块
    extension.init()

    # 创建 FastAPI 应用
    app = FastAPI(**config.app, lifespan=event.lifespan)

    # 注册中间件
    middleware.register(app)

    # 注册路由
    app.include_router(api_router)

    return app
