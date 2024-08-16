"""主路由模块."""

from fastapi import APIRouter

from src.api.lark.router import router as lark_router_api_v1
from src.api.web.router import router as web_router_api_v1
from src.lib import enum


api_router = APIRouter()

api_router.include_router(lark_router_api_v1, prefix=f"/api/v{enum.ApiVersion.VERSION_1.value}/lark", tags=["lark"])
api_router.include_router(web_router_api_v1, prefix=f"/api/v{enum.ApiVersion.VERSION_1.value}/web", tags=["web"])


@api_router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """健康检查."""
    return {"status": "ok"}
