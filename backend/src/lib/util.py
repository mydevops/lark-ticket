"""工具模块."""

import base64
import hashlib
import socket
import time
from typing import Any

import httpx
import orjson
from Crypto.Cipher import AES
from loguru import logger

from src.lib import const
from src.lib import enum
from src.lib import schema
from src.lib.config import settings


def make_response_ok(resp: dict[str, Any] | None = None) -> dict[str, Any]:
    """构造成功的响应格式.

    Args:
        resp: 返回的数据.

    Returns:
        成功的响应字典.
    """
    return {
        "retcode": enum.HTTPBusinessStatusCode.SUCCESS.value,
        "msg": const.HTTP_MAKE_RESPONSE_OK_MSG,
        "resp": resp if resp else {},
        "error": "",
    }


def make_response_not_ok(error: str) -> dict[str, Any]:
    """构造失败的响应格式.

    Args:
        error: 错误描述.

    Returns:
        失败的响应字典.
    """
    return {
        "retcode": enum.HTTPBusinessStatusCode.FAILURE.value,
        "error": error,
        "msg": "",
        "resp": {},
    }


def scheduler_lock() -> bool:
    """尝试获取调度锁.

    Returns:
        如果锁已经被占用，返回 True 否则返回 False.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((settings.scheduler_lock.host, settings.scheduler_lock.port))
    except OSError:
        return True
    else:
        time.sleep(const.SCHEDULER_DETECTION_INTERVAL_SECOND)
        return False


def log_format(response: httpx.Response, title: str, desc: str) -> str:
    """格式化日志信息.

    Args:
        response: httpx 响应对象.
        title: 日志标题.
        desc: 日志描述.

    Returns:
        格式化后的日志字符串.
    """
    return (
        f"[{title}] {desc} - {response.request.method} - url: {response.url} header: {dict(response.request.headers)} "
        f"body: {response.request.content.decode()} response: {response.text}"
    )


async def do_post(url: str, data: dict, header: dict | None = None) -> schema.LarkCheckOrExecuteCallback:
    """发送 POST 请求.

    Args:
        url: 请求的 URL.
        data: 请求体数据.
        header: 请求头，默认为 None.

    Returns:
        LarkCheckOrExecuteCallback 对象.
    """
    async with httpx.AsyncClient(
        headers={**const.HTTP_JSON_HEADER, **(header or {})},
        timeout=const.HTTP_REQUEST_TIMEOUT_SECONDS,
    ) as client:
        r = await client.post(url, json=data)
        logger.info(log_format(r, __name__, "send post request"))
        assert r.status_code in const.HTTP_SUCCESS_STATUS_CODE, r.text
        return schema.LarkCheckOrExecuteCallback(**r.json())


async def do_get(url: str, params: dict, header: dict | None = None) -> dict[str, Any]:
    """发送 GET 请求.

    Args:
        url: 请求的 URL.
        params: 请求参数.
        header: 请求头，默认为 None.

    Returns:
        请求的响应数据.
    """
    async with httpx.AsyncClient(
        headers={**const.HTTP_JSON_HEADER, **(header or {})},
        timeout=const.HTTP_REQUEST_TIMEOUT_SECONDS,
    ) as client:
        r = await client.get(url, params=params)
        logger.info(log_format(r, __name__, "send get request"))
        assert r.status_code in const.HTTP_SUCCESS_STATUS_CODE, r.text
        return r.json()


class _AESCipher:
    """解密."""

    def __init__(self, key: str | bytes) -> None:
        """初始化 AES 解密器.

        Args:
            key: 用于解密的密钥，可以是字符串或字节.
        """
        if isinstance(key, str):
            key = key.encode(const.UTF_8)
        self.digest = hashlib.sha256(key).digest()

    def decrypt(self, enc: bytes) -> bytes:
        """解密数据.

        Args:
            enc: 加密后的数据.

        Returns:
            解密后的数据.
        """
        iv = enc[: AES.block_size]
        cipher = AES.new(self.digest, AES.MODE_CBC, iv)
        n_ = AES.block_size
        s = cipher.decrypt(enc[n_:])
        m_ = len(s) - 1
        return s[: -ord(s[m_:])]

    def decrypt_str(self, enc: str | bytes) -> str:
        """解密字符串.

        Args:
            enc: 加密的字符串，可以是字符串或字节.

        Returns:
            解密后的字符串.
        """
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode(const.UTF_8)


def decrypt(content: str) -> schema.LarkEventContext:
    """解密内容并转换为 LarkEventContext 对象.

    Args:
        content: 加密的内容.

    Returns:
        LarkEventContext 对象.
    """
    return schema.LarkEventContext(**orjson.loads(_AESCipher(settings.lark.encrypt_key).decrypt_str(content)))
