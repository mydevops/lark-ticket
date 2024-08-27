"""路由处理逻辑."""

from typing import Any

import orjson
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import ConfigModel
from src.lib import const
from src.lib import schema
from src.lib import util
from src.lib.call import lark_api
from src.lib.config import enum
from src.lib.config import settings
from src.lib.extension import handle_exceptions


@handle_exceptions
async def callback_approval_task(session: AsyncSession, body: schema.LarkEventContext):
    """处理审批任务状态变更的回调.

    Args:
        session: 数据库会话.
        body: 状态结构.
    """
    # 仅处理"审批助手"和"审批中"的消息
    if (
        body.event.get("user_id", "") == settings.lark.assistant_user_id
        and body.event.get("status") == const.LARK_CALLBACK_APPROVAL_TASK_STATUS
    ):
        metadata: dict[str, Any] = {}

        approval_instance_detail = await lark_api.get_approval_instance_detail(body.event.get("instance_code", ""))

        config: schema.Config = await ConfigModel.get(session, approval_instance_detail.approval_code)

        # 通过关联字段进行转换
        if config.relation.is_open:
            for component in orjson.loads(approval_instance_detail.form):
                _relation = {item.code: item.api_key for item in config.relation.data}
                if component.get("id") in _relation:
                    metadata[_relation.get(component.get("id"), "")] = component

        task = approval_instance_detail.task_list[-1]

        ticket_id = (
            f"{approval_instance_detail.approval_code}"
            f"{const.LARK_TICKET_ID_DELIMITER}"
            f"{approval_instance_detail.instance_code}"
            f"{const.LARK_TICKET_ID_DELIMITER}"
            f"{task.id}"
        )
        metadata["ticket_id"] = ticket_id

        # 检查节点
        if task.node_name == const.LARK_CHECK_NODE_NAME and task.status == const.LARK_CHECK_NODE_TASK_STATUS:
            if config.check.is_open:
                if config.check.call_type == enum.APICallType.SYNC:
                    await check_callback(await util.do_post(config.check.url, metadata))
                elif config.check.call_type == enum.APICallType.ASYNC:
                    await util.do_post(config.check.url, metadata)
            else:
                await check_callback(
                    schema.LarkCheckOrExecuteCallback(ticket_id=ticket_id, result=True, msg="", error="")
                )
        # 执行节点
        elif task.node_name == const.LARK_EXECUTE_NODE_NAME and task.status == const.LARK_EXECUTE_NODE_TASK_STATUS:
            if config.execute.is_open:
                if config.execute.call_type == enum.APICallType.SYNC:
                    await check_callback(await util.do_post(config.execute.url, metadata))
                elif config.execute.call_type == enum.APICallType.ASYNC:
                    await util.do_post(config.execute.url, metadata)
            else:
                await execute_callback(
                    schema.LarkCheckOrExecuteCallback(ticket_id=ticket_id, result=True, msg="", error="")
                )


@handle_exceptions
async def check_callback(params: schema.LarkCheckOrExecuteCallback):
    """处理检查回调."""
    approval_code, instance_code, task_id = params.ticket_id.split(const.LARK_TICKET_ID_DELIMITER)

    # 检查成功: 审批通过
    if params.result:
        await lark_api.approval_task_approve(
            approval_code, instance_code, task_id, params.msg or const.LARK_CHECK_SUCCESS_DEFAULT_COMMENT
        )
    # 检查失败: 审批拒绝
    else:
        await lark_api.approval_task_reject(
            approval_code, instance_code, task_id, params.error or const.LARK_CHECK_FAILURE_DEFAULT_COMMENT
        )


@handle_exceptions
async def execute_callback(params: schema.LarkCheckOrExecuteCallback):
    """处理执行回调."""
    approval_code, instance_code, task_id = params.ticket_id.split(const.LARK_TICKET_ID_DELIMITER)

    # 执行成功: 审批通过
    if params.result:
        await lark_api.approval_task_approve(
            approval_code, instance_code, task_id, params.msg or const.LARK_CHECK_SUCCESS_DEFAULT_COMMENT
        )
    # 执行失败: 审批拒绝
    else:
        await lark_api.approval_task_reject(
            approval_code, instance_code, task_id, params.error or const.LARK_CHECK_FAILURE_DEFAULT_COMMENT
        )


async def external_field(session: AsyncSession, approval_code: str, field_code: str, params: schema.LarkExternalField):
    """获取外部字段数据."""
    config: schema.Config = await ConfigModel.get(session, approval_code)
    _field_map = {item.code: item.url for item in config.field.data}
    return util.do_post(_field_map.get(field_code, ""), params.dict())
