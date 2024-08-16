"""拓展模块.

loguru 配置.
sentry 配置.
异常捕获.
"""

import logging
import os
from collections.abc import Callable
from collections.abc import Coroutine
from functools import wraps
from typing import Any

import sentry_sdk
from loguru import logger

from src.lib import enum
from src.lib import exceptions
from src.lib.config import settings


class InterceptHandler(logging.Handler):
    """自定义日志处理."""

    def emit(self, record: logging.LogRecord) -> None:
        """将日志记录转发到 loguru."""
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def _configure_logging():
    """配置 loguru."""
    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    # 移除 uvicorn 的默认处理器
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []

    # 为 uvicorn 和 fastapi 设置日志处理器
    for _log in ["uvicorn", "uvicorn.access", "fastapi"]:
        logging.getLogger(_log).handlers = [intercept_handler]

    logger.remove()
    logger.add(
        os.path.join(settings.loguru.path, settings.loguru.filename),
        rotation=settings.loguru.rotation,
        enqueue=True,
        backtrace=True,
        level=settings.loguru.level.upper(),
        format=settings.loguru.format,
    )


def ignore_exception(event: Any, hint: Any) -> Any:
    """自定义函数，忽略特定异常后再发送到 Sentry.

    Args:
        event: 要发送到 Sentry 的事件.
        hint: 异常的附加信息.

    Returns:
        事件如果应该发送，或者 None 如果应该被忽略.
    """
    if isinstance(hint, dict) and "exc_info" in hint:
        _, exc_value, _ = hint["exc_info"]
        if isinstance(exc_value, exceptions.IgnoreException):
            return None
    return event


def _configure_sentry() -> None:
    """初始化 Sentry SDK."""
    sentry_sdk.init(
        dsn=settings.alarm.sentry_dsn,
        enable_tracing=True,
        before_send=ignore_exception,
    )


def handle_exceptions(
    task_function: Callable[..., Coroutine[Any, Any, Any]],
) -> Callable[..., Coroutine[Any, Any, Any]]:
    """装饰器,用于处理异步函数中的异常.

    Args:
        task_function: 要包装的异步函数.

    Returns:
        包装后的异步函数，记录异常并将其发送到 Sentry
    """

    @wraps(task_function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await task_function(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            sentry_sdk.capture_exception(e)

    return wrapper


def init() -> None:
    """初始化扩展."""
    # loguru
    _configure_logging()

    # sentry
    if (
        settings.basic.debug is False
        and settings.alarm.open
        and settings.alarm.notification_type == enum.AlarmNotificationType.SENTRY
    ):
        _configure_sentry()
