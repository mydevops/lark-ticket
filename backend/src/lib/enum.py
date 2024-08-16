"""枚举模块."""

from enum import Enum
from enum import unique


@unique
class ApiVersion(Enum):
    """API 版本枚举."""

    VERSION_1 = 1
    VERSION_2 = 2
    VERSION_3 = 3
    VERSION_4 = 4
    VERSION_5 = 5

    def __str__(self):
        """返回 API 版本的字符串表示形式."""
        return f"API Version {self.value}"


@unique
class HTTPBusinessStatusCode(Enum):
    """HTTP 业务状态码枚举."""

    SUCCESS = 0
    FAILURE = -1

    def __str__(self):
        """返回 HTTP 业务状态码的字符串表示形式."""
        return "success" if self == HTTPBusinessStatusCode.SUCCESS else "failure"


@unique
class AlarmNotificationType(str, Enum):
    """报警通知类型枚举."""

    SENTRY = "sentry"

    def __str__(self):
        """返回报警通知类型的字符串表示形式."""
        return f"alarm notification type {self.value}"


@unique
class APICallType(str, Enum):
    """API 调用类型枚举."""

    SYNC = "sync"
    ASYNC = "async"

    def __str__(self):
        """返回 API 调用类型的字符串表示形式."""
        return f"api call type {self.value}"
