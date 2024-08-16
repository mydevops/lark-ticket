"""配置文件模块."""

import configparser
import os
from typing import Any

from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic import ValidationError

from src.lib import const
from src.lib import enum


class Basic(BaseModel):
    """基础配置."""

    app_name: str
    host: str
    port: int
    workers_count: int
    debug: bool


class Loguru(BaseModel):
    """日志配置."""

    path: str
    filename: str
    level: str
    rotation: str
    format: str


class MySQL(BaseModel):
    """MySQL 数据库配置."""

    dsn: str


class SchedulerLock(BaseModel):
    """锁配置.

    当前是使用端口占用的方式实现，主要用途是多进程时定时任务和初始化表的锁。
    """

    host: str
    port: int


class Alarm(BaseModel):
    """报警配置.

    目前仅支持 Sentry.
    """

    open: bool = False
    notification_type: enum.AlarmNotificationType | None = None
    sentry_dsn: str | None = None


class Lark(BaseModel):
    """飞书配置."""

    assistant_user_id: str
    domain: str
    app_id: str
    app_secret: str
    encrypt_key: str
    verification_token: str


class App(BaseModel):
    """集成类,包含所有配置."""

    basic: Basic
    loguru: Loguru
    mysql: MySQL
    scheduler_lock: SchedulerLock
    alarm: Alarm
    lark: Lark


def read_config(file_path: str) -> App:
    """读取配置文件并返回 APP 配置对象."""
    config = configparser.ConfigParser()

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"配置文件未找到: {file_path}")

    config.read(file_path)

    try:
        mysql_config = config["MYSQL"]

        return App(
            basic=Basic(**config["BASIC"]),
            loguru=Loguru(**config["LOGURU"]),
            mysql=MySQL(
                dsn=f"{mysql_config.get('scheme', '')}://{mysql_config.get('user', '')}:{mysql_config.get('password', '')}@"
                f"{mysql_config.get('host', '')}:{mysql_config.get('port', '')}/{mysql_config.get('db', '')}"
            ),
            scheduler_lock=SchedulerLock(**config["SCHEDULERLOCK"]),
            alarm=Alarm(**config["ALARM"]),
            lark=Lark(**config["LARK"]),
        )
    except KeyError as e:
        raise ValueError(f"缺少配置部分: {e}")
    except ValidationError as e:
        raise ValidationError(f"配置验证错误: {e}")


# 读取配置
settings = read_config(const.BASIC_CONFIG_PATH)


# FastAPI 配置
app: dict[str, Any] = {
    "title": f"{settings.basic.app_name} API",
    "default_response_class": ORJSONResponse,
}
