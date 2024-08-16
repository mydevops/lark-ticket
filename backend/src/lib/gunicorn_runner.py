"""Gunicorn 初始化模块."""

from typing import Any

from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from uvicorn_worker import UvicornWorker as BaseUvicornWorker

from src.lib import const


class UvicornWorker(BaseUvicornWorker):
    """配置 Uvicorn 以便与 Gunicorn 一起使用."""

    CONFIG_KWARGS = {
        "loop": const.UVICORN_PARAM_LOOP,
        "http": const.UVICORN_PARAM_HTTP,
        "lifespan": const.UVICORN_PARAM_LIFESPAN,
        "factory": const.UVICORN_PARAM_FACTORY,
    }


class GunicornApplication(BaseApplication):
    """将 Gunicorn 与 Uvicorn 集成."""

    def __init__(self, app: str, host: str, port: int, workers: int, worker_class: str, **kwargs: Any):
        """初始化 Gunicorn 应用程序.

        Args:
            app: 应用程序路径（字符串形式）.
            host: 要绑定的主机地址.
            port: 要绑定的端口号.
            workers: 工作进程的数量.
            worker_class: Gunicorn 要使用的工作类.
            **kwargs: 其他 Gunicorn 配置选项.
        """
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": worker_class,
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        """将配置选项加载到 Gunicorn."""
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self) -> str:
        """加载应用程序."""
        return import_app(self.app)
