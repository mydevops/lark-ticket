"""路由模块."""

from fastapi import APIRouter
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.web import service
from src.db.base import get_db_session
from src.lib import schema
from src.lib import util


router = APIRouter()


@router.get("/configs", response_model=schema.HTTPResponse)
async def get_configs(session: AsyncSession = Depends(get_db_session)):
    """获取所有审批定义配置.

    Args:
        session: 数据库会话.

    Returns:
        包含所有配置的数据.
    """
    logger.info("[web][received get configs]")
    return util.make_response_ok(await service.get_configs(session))


@router.get("/config/{approval_code}", response_model=schema.HTTPResponse)
async def get_config(approval_code: str, session: AsyncSession = Depends(get_db_session)):
    """获取指定审批定义 code 的配置.

    Args:
        approval_code: 审批定义 code.
        session: 数据库会话.

    Returns:
        指定审批定义 code 的配置数据.
    """
    logger.info(f"[web][received get config] approval_code: {approval_code}")
    return util.make_response_ok(await service.get_config(session, approval_code))


@router.post("/config", response_model=schema.HTTPResponse)
async def create_config(body: schema.Config, session: AsyncSession = Depends(get_db_session)):
    """创建审批定义配置.

    Args:
        body: 配置信息.
        session: 数据库会话.

    Returns:
        配置创建成功.
    """
    logger.info(f"[web][received create config] approval_code: {body.approval_code}")
    await service.create_config(session, body)
    return util.make_response_ok()


@router.put("/config", response_model=schema.HTTPResponse)
async def update_config(body: schema.Config, session: AsyncSession = Depends(get_db_session)):
    """更新审批定义配置.

    Args:
        body: 更新后的配置信息.
        session: 数据库会话.

    Returns:
        配置更新成功.
    """
    logger.info(f"[web][received update config] approval_code: {body.approval_code}")
    await service.update_config(session, body)
    return util.make_response_ok()


@router.delete("/config/{approval_code}", response_model=schema.HTTPResponse)
async def delete_config(approval_code: str, session: AsyncSession = Depends(get_db_session)):
    """删除指定审批定义配置.

    Args:
        approval_code: 审批定义 code.
        session: 数据库会话.

    Returns:
        删除成功.
    """
    logger.info(f"[web][received delete config] approval_code: {approval_code}")
    await service.delete_config(session, approval_code)
    return util.make_response_ok()


@router.get("/lark/approval/fields", response_model=schema.HTTPResponse)
async def get_lark_approval_fields(approval_code: str):
    """获取飞书审批定义 form 字段信息.

    Args:
        approval_code: 审批定义 code.

    Returns:
        具体的配置.
    """
    logger.info(f"[web][received get lark approval fields] approval_code: {approval_code}")
    return util.make_response_ok(await service.get_lark_approval_fields(approval_code))
