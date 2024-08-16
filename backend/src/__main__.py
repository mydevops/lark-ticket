"""rye run dev 运行的就是这个文件.

等同于运行 python -m src

具体配置在 pyproject.toml 中
dev = "python -m src"
"""

import uvicorn

from src.lib import const
from src.lib.config import settings
from src.lib.gunicorn_runner import GunicornApplication


def main():
    """程序入口函数."""
    if settings.basic.debug:
        # 启动 Uvicorn 服务器
        uvicorn.run(
            app=const.BASIC_MAIN_APP_PATH,
            host=settings.basic.host,
            port=settings.basic.port,
            workers=settings.basic.workers_count,
            log_level=settings.loguru.level,
            reload=settings.basic.debug,
            factory=const.UVICORN_PARAM_FACTORY,
        )
    else:
        # 启动 Gunicorn 服务器
        GunicornApplication(
            app=const.BASIC_MAIN_APP_PATH,
            host=settings.basic.host,
            port=settings.basic.port,
            workers=settings.basic.workers_count,
            worker_class="src.lib.gunicorn_runner.UvicornWorker",
            loglevel=settings.loguru.level,
            factory=const.GUNICORN_PARAM_FACTORY,
        ).run()


if __name__ == "__main__":
    main()
