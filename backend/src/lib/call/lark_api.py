"""飞书 SDK 封装."""

import lark_oapi as lark
from lark_oapi.api.approval.v4 import ApproveTaskRequest
from lark_oapi.api.approval.v4 import ApproveTaskResponse
from lark_oapi.api.approval.v4 import GetApprovalRequest
from lark_oapi.api.approval.v4 import GetApprovalResponse
from lark_oapi.api.approval.v4 import GetApprovalResponseBody
from lark_oapi.api.approval.v4 import GetInstanceRequest
from lark_oapi.api.approval.v4 import GetInstanceResponse
from lark_oapi.api.approval.v4 import GetInstanceResponseBody
from lark_oapi.api.approval.v4 import RejectTaskRequest
from lark_oapi.api.approval.v4 import RejectTaskResponse
from lark_oapi.api.approval.v4 import SubscribeApprovalRequest
from lark_oapi.api.approval.v4 import SubscribeApprovalResponse
from lark_oapi.api.approval.v4 import TaskApprove
from lark_oapi.api.approval.v4 import UnsubscribeApprovalRequest
from lark_oapi.api.approval.v4 import UnsubscribeApprovalResponse

from src.lib.config import settings


_client = (
    lark.Client.builder()
    .app_id(settings.lark.app_id)
    .app_secret(settings.lark.app_secret)
    .log_level(lark.LogLevel.DEBUG)
    .build()
)


async def get_approval_instance_detail(instance_id: str) -> GetInstanceResponseBody:
    """获取审批实例的详细信息.

    Args:
        instance_id: 审批实例的 ID.

    Returns:
        GetInstanceResponseBody: 审批实例的详细信息.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: GetInstanceRequest = GetInstanceRequest.builder().instance_id(instance_id).build()
    response: GetInstanceResponse = await _client.approval.v4.instance.aget(request)

    if not response.success():
        raise Exception(
            f"[get_approval_instance_detail failed] code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}"
        )
    return response.data


async def approval_task_approve(approval_code: str, instance_code: str, task_id: str, comment: str):
    """批准审批任务.

    Args:
        approval_code: 审批定义 code.
        instance_code: 实例代码.
        task_id: 任务 ID.
        comment: 评论.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: ApproveTaskRequest = (
        ApproveTaskRequest.builder()
        .user_id_type("user_id")
        .request_body(
            TaskApprove.builder()
            .approval_code(approval_code)
            .instance_code(instance_code)
            .user_id(settings.lark.assistant_user_id)
            .comment(comment)
            .task_id(task_id)
            .build()
        )
        .build()
    )

    response: ApproveTaskResponse = await _client.approval.v4.task.aapprove(request)
    if not response.success():
        raise Exception(
            f"[approval_task_approve failed] code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}"
        )


async def approval_task_reject(approval_code: str, instance_code: str, task_id: str, comment: str):
    """拒绝审批任务.

    Args:
        approval_code: 审批定义 code.
        instance_code: 实例代码.
        task_id: 任务 ID.
        comment: 评论.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: RejectTaskRequest = (
        RejectTaskRequest.builder()
        .user_id_type("user_id")
        .request_body(
            TaskApprove.builder()
            .approval_code(approval_code)
            .instance_code(instance_code)
            .user_id(settings.lark.assistant_user_id)
            .comment(comment)
            .task_id(task_id)
            .build()
        )
        .build()
    )
    response: RejectTaskResponse = await _client.approval.v4.task.areject(request)
    if not response.success():
        raise Exception(
            f"[approval_task_reject failed] code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
        )


async def get_approval_detail(approval_code: str) -> GetApprovalResponseBody:
    """获取审批定义详情.

    Args:
        approval_code: 审批定义 code.

    Returns:
        GetApprovalResponseBody: 审批详情.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: GetApprovalRequest = GetApprovalRequest.builder().approval_code(approval_code).build()
    response: GetApprovalResponse = await _client.approval.v4.approval.aget(request)
    if not response.success():
        raise Exception(
            f"[get_approval_detail failed] code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
        )
    return response.data


async def subscribe_approval_callback_event(approval_code: str):
    """订阅审批回调事件.

    Args:
        approval_code: 审批定义 code.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: SubscribeApprovalRequest = SubscribeApprovalRequest.builder().approval_code(approval_code).build()
    response: SubscribeApprovalResponse = await _client.approval.v4.approval.asubscribe(request)
    if not response.success():
        raise Exception(
            f"[subscribe_approval_callback_event failed] code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}"
        )


async def unsubscribe_approval_callback_event(approval_code: str):
    """取消订阅审批回调事件.

    Args:
        approval_code: 审批定义 code.

    Raises:
        Exception: 如果请求失败，则抛出异常.
    """
    request: UnsubscribeApprovalRequest = UnsubscribeApprovalRequest.builder().approval_code(approval_code).build()
    response: UnsubscribeApprovalResponse = _client.approval.v4.approval.unsubscribe(request)
    if not response.success():
        raise Exception(
            f"[unsubscribe_approval_callback_event failed] code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}"
        )
