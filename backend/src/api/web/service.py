"""路由处理逻辑."""

from typing import Any

import orjson
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import ConfigModel
from src.lib import schema
from src.lib.call import lark_api
from src.lib.exceptions import IgnoreException


async def get_configs(session: AsyncSession) -> dict[str, str]:
    """获取所有审批定义配置."""
    entries_stmt = (
        select(ConfigModel.approval_code, ConfigModel.name)
        .filter(ConfigModel.id != -1)
        .order_by(ConfigModel.create_time)
    )

    response: dict[str, Any] = {"body": []}

    for entry in await session.execute(entries_stmt):
        response["body"].append({"approval_code": entry.approval_code, "name": entry.name})

    return response


async def get_config(session: AsyncSession, approval_code: str) -> dict[str, Any]:
    """获取指定审批定义 code 的配置."""
    if not await ConfigModel.exists(session, approval_code):
        raise IgnoreException(f"approval_code: {approval_code} does not exist!")

    config: schema.Config = await ConfigModel.get(session, approval_code)

    response: dict[str, Any] = {
        "approval_code": config.approval_code,
        "name": config.name,
        "check": config.check,
        "execute": config.execute,
        "field": config.field,
        "relation": config.relation,
    }

    return response


async def create_config(session: AsyncSession, body: schema.Config):
    """创建审批定义配置."""
    if await ConfigModel.exists(session, body.approval_code):
        raise IgnoreException(f"approval_code: {body.approval_code} already exists!")

    await session.execute(
        insert(ConfigModel).values(
            approval_code=body.approval_code,
            name=body.name,
            check=body.check.dict(),
            execute=body.execute.dict(),
            field=body.field.dict(),
            relation=body.relation.dict(),
        )
    )

    await lark_api.subscribe_approval_callback_event(body.approval_code)

    await session.commit()


async def update_config(session: AsyncSession, body: schema.Config):
    """更新审批定义配置."""
    if not await ConfigModel.exists(session, body.approval_code):
        raise IgnoreException(f"approval_code: {body.approval_code} does not exist!")

    await session.execute(
        update(ConfigModel)
        .where(ConfigModel.approval_code == body.approval_code)
        .values(
            {
                "name": body.name,
                "check": body.check.dict(),
                "execute": body.execute.dict(),
                "field": body.field.dict(),
                "relation": body.relation.dict(),
            }
        )
    )
    await session.commit()


async def delete_config(session: AsyncSession, approval_code: str) -> None:
    """删除指定审批定义配置."""
    if not await ConfigModel.exists(session, approval_code):
        raise IgnoreException(f"approval_code: {approval_code} does not exist!")

    await session.execute(delete(ConfigModel).where(ConfigModel.approval_code == approval_code))

    await lark_api.unsubscribe_approval_callback_event(approval_code)

    await session.commit()


async def get_lark_approval_fields(approval_code: str):
    """获取飞书审批定义 form 字段信息."""
    response = await lark_api.get_approval_detail(approval_code)
    return {"body": [{"label": field.get("name"), "value": field.get("id")} for field in orjson.loads(response.form)]}
