"""结构体模块."""

from typing import Any

from pydantic import BaseModel
from pydantic import Field

from src.lib import enum


class HTTPResponse(BaseModel):
    """通用 HTTP 响应格式."""

    retcode: int = Field(description="返回状态码：0 表示成功，其他值表示失败")
    msg: str = Field("", description="成功消息")
    error: str = Field("", description="错误描述")
    resp: dict[Any, Any] = Field({}, description="具体数据")


class LarkEncryptRequest(BaseModel):
    """飞书回调加密请求的结构."""

    encrypt: str = Field(description="加密字符串")


class LarkEventHeader(BaseModel):
    """飞书回调事件的 header 信息."""

    event_id: str | None = Field(None, description="唯一事件标识符")
    token: str | None = Field(None, description="验证令牌")
    create_time: str | None = Field(None, description="事件发送的时间戳")
    event_type: str | None = Field(None, description="事件类型")
    tenant_key: str | None = Field(None, description="租户密钥")
    app_id: str | None = Field(None, description="应用标识符")


class LarkEventContext(BaseModel):
    """飞书回调解密后的结构."""

    challenge: str | None = Field(None, description="注册验证字段")
    ts: str | None = Field(None, description="时间戳(v1.0)")
    uuid: str | None = Field(None, description="唯一标识符(v1.0)")
    token: str | None = Field(None, description="验证令牌(v1.0)")
    type: str | None = Field(None, description="事件类型(v1.0)")
    schema_: str | None = Field(None, alias="schema", description="结构体(v2.0)")
    header: LarkEventHeader | None = Field(None, description="元数据(v2.0)")
    event: dict = Field({}, description="事件详情(all versions)")


class LarkCheckOrExecuteCallback(BaseModel):
    """检查或执行节点的回调结构."""

    ticket_id: str = Field(description="工单标识符")
    result: bool = Field(description="检查或执行结果: True 成功 False 失败")
    msg: str = Field("", description="成功消息")
    error: str = Field("", description="错误描述")


class LarkExternalField(BaseModel):
    """飞书外部字段调用参数."""

    linkage_params: dict[str, Any] = Field(default_factory=dict, description="具体参数")
    token: str | None = Field(None, description="校验请求是否为合法来源的 token")
    page_token: str | None = Field(None, description="分页标记，第一次请求不填，表示从头开始遍历")
    query: str | None = Field(None, description="搜索关键词")


class CheckConfig(BaseModel):
    """检查节点配置."""

    is_open: bool = Field(description="是否开启检查节点: True 开启 False 关闭")
    url: str = Field("", description="检查请求的 api 地址")
    call_type: enum.APICallType = Field(description="请求类型")


class ExecuteConfig(BaseModel):
    """执行节点配置."""

    is_open: bool = Field(description="是否开启执行节点: True 开启 False 关闭")
    url: str = Field("", description="执行请求的 api 地址")
    call_type: enum.APICallType = Field(description="请求类型")


class FieldItem(BaseModel):
    """外部字段的动态配置."""

    code: str = Field(description="飞书字段唯一标识")
    url: str = Field(description="请求地址")


class FieldConfig(BaseModel):
    """外部字段配置."""

    is_open: bool = Field(description="是否开启外部字段: True 开启 False 关闭")
    data: list[FieldItem] = Field(description="动态配置")


class RelationItem(BaseModel):
    """字段关联的动态配置."""

    code: str = Field(description="飞书字段唯一标识")
    api_key: str = Field(description="要转换成的字段名称")


class RelationConfig(BaseModel):
    """字段关联关系配置."""

    is_open: bool = Field(description="是否开启字段关联: True 开启 False 关闭")
    data: list[RelationItem] = Field(description="动态配置")


class Config(BaseModel):
    """审批配置."""

    approval_code: str
    name: str
    check: CheckConfig
    execute: ExecuteConfig
    field: FieldConfig
    relation: RelationConfig
