"""路由模块."""

from asyncer import asyncify
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.lark import service
from src.db.base import get_db_session
from src.db.config import ConfigModel
from src.lib import const
from src.lib import schema
from src.lib import util


router = APIRouter()


@router.post("/callback")
async def callback(
    background_tasks: BackgroundTasks,
    encryption_body: schema.LarkEncryptRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """处理来自飞书的回调请求.

    Args:
        background_tasks: 后台任务.
        encryption_body: 加密请求体.
        session: 数据库会话.

    Returns:
        dict[str, str]: 返回处理结果.
    """
    body: schema.LarkEventContext = await asyncify(util.decrypt)(encryption_body.encrypt)
    logger.info(f"[lark][received callback]: {body}")
    if body.type == const.LARK_URL_VERIFICATION:
        return {"challenge": body.challenge or ""}

    # 兼容 v1 和 v2 回调格式
    if body.schema_:
        if hasattr(body.header, "event_type"):
            body.type = getattr(body.header, "event_type")
    else:
        body.type = body.event.get("type")

    # 检查授权
    if await ConfigModel.exists(session, body.event.get("approval_code", "")):
        background_tasks.add_task(getattr(service, f"callback_{body.type}"), session, body)
    else:
        logger.info(f"[lark][ignore unauthorized approvals] approval_code: {body.event.get('approval_code', '')}")

    return {"msg": "success"}


@router.post("/check/callback", response_model=schema.HTTPResponse)
async def check_callback(background_tasks: BackgroundTasks, params: schema.LarkCheckOrExecuteCallback):
    """检查节点回调.

    Args:
        background_tasks: 后台任务.
        params: 请求参数.

    Returns:
        schema.HTTPResponse: 返回 HTTP 响应.
    """
    logger.info(f"[lark][received check callback]: {params}")
    background_tasks.add_task(service.check_callback, params)
    return util.make_response_ok()


@router.post("/execute/callback", response_model=schema.HTTPResponse)
async def execute_callback(background_tasks: BackgroundTasks, params: schema.LarkCheckOrExecuteCallback):
    """执行节点回调.

    Args:
        background_tasks: 后台任务.
        params: 请求参数.

    Returns:
        schema.HTTPResponse: 返回 HTTP 响应.
    """
    logger.info(f"[received execute callback]: {params}")
    background_tasks.add_task(service.execute_callback, params)
    return util.make_response_ok()


@router.get("/field/{approval_code}/{field_code}")
async def external_field(
    approval_code: str,
    field_code: str,
    params: schema.LarkExternalField,
    session: AsyncSession = Depends(get_db_session),
):
    """获取外部字段数据.

    Args:
        approval_code: 审批定义 code.
        field_code: 审批字段 code.
        params: 请求参数.
        session: 数据库会话.

    Returns:
        飞书所需的字段格式.
    """
    logger.info(f"[lark][received external field]: {params}")
    return await service.external_field(session, approval_code, field_code, params)
