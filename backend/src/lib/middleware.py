"""中间件模块.

1. 请求响应时间中间件
2. 异常捕获中间件
"""

import time
from typing import Any

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from src.lib import enum
from src.lib import exceptions
from src.lib import util
from src.lib.config import settings


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    """记录请求响应时间的中间件."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Any:
        """处理请求并记录响应时间."""
        start_time = time.time()
        response = await call_next(request)
        if request.url.path != "/healthcheck" and "form-data" not in request.headers.get("content-type", ""):
            logger.info(
                f"response: Method {request.method} - {request.url.path} - "
                f"code: {response.status_code} "
                f"{(time.time() - start_time) * 1000:.2f}ms"
            )
        return response


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    """捕获和记录异常的中间件，并返回 JSON 响应."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """处理请求并捕获异常."""
        try:
            return await call_next(request)
        except Exception as e:
            if not isinstance(e, exceptions.IgnoreException):
                logger.exception(e)
            return ORJSONResponse(util.make_response_not_ok(str(e)))


def register(app: FastAPI):
    """注册中间件和异常处理程序.

    Args:
        app: FastAPI 实例.
    """
    app.add_middleware(ResponseTimeMiddleware)  # type: ignore
    if (
        settings.basic.debug is False
        and settings.alarm.open
        and settings.alarm.notification_type == enum.AlarmNotificationType.SENTRY
    ):
        app.add_middleware(SentryAsgiMiddleware)  # type: ignore
    app.add_middleware(CatchExceptionsMiddleware)  # type: ignore

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Any, exc: Any) -> ORJSONResponse:
        """处理请求验证错误."""
        return ORJSONResponse(util.make_response_not_ok(str(exc.errors())))

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, _: Any) -> ORJSONResponse:
        """处理 404 错误."""
        return ORJSONResponse(
            util.make_response_not_ok(f"[{request.url.path}] Not Found"),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(405)
    async def custom_405_handler(request: Request, _: Any) -> ORJSONResponse:
        """处理 405 错误."""
        return ORJSONResponse(
            util.make_response_not_ok(f"{request.method} [{request.url.path}] Method Not Allowed"),
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
