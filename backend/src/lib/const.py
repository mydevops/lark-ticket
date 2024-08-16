"""常量模块."""

import os


UTF_8 = "UTF-8"

#######################################
# BASIC
#######################################
# 配置文件路径
BASIC_CONFIG_PATH = os.path.join("etc", "lark-ticket.conf")
# 初始化 FastAPI 实例的函数路径
BASIC_MAIN_APP_PATH = "src.app:make_app"
# Python 文件后缀
BASIC_PYTHON_FILE_SUFFIX = ".py"

#######################################
# HTTP
#######################################
# 响应成功消息
HTTP_MAKE_RESPONSE_OK_MSG = "success"
# JSON 请求头
HTTP_JSON_HEADER = {"Content-Type": "application/json"}
# 请求超时时间(秒)
HTTP_REQUEST_TIMEOUT_SECONDS = 5
# 成功状态码
HTTP_SUCCESS_STATUS_CODE = [200]

#######################################
# UVICORN
#######################################
# 事件循环类型
UVICORN_PARAM_LOOP = "uvloop"
# HTTP 工具类型
UVICORN_PARAM_HTTP = "httptools"
# 生命周期管理开关
UVICORN_PARAM_LIFESPAN = "on"
# 是否启用工厂模式
UVICORN_PARAM_FACTORY = True

#######################################
# GUNICORN
#######################################
# 是否启用工厂模式
GUNICORN_PARAM_FACTORY = True
# uvicorn 主类
GUNICORN_WORKER_CLASS = "src.lib.gunicorn_runner.UvicornWorker"

#######################################
# DATABASE
#######################################
# 数据库包根路径
DATABASE_ROOT = "src.db"
# 插件需要排除的文件列表
DATABASE_EXCLUDE_FILE = ["__init__.py", "base.py"]
# 主键
DATABASE_FIELD_ID_PRIMARY_KEY = True
# id 自增
DATABASE_FIELD_ID_AUTOINCREMENT = True
# 排序优先级，越小越靠前。
DATABASE_FIELD_ID_SORT_ORDER = -1
# 创建时间
DATABASE_FIELD_CREATETIME_SERVER_DEFAULT = "CURRENT_TIMESTAMP"
# 创建时间字段优先级
DATABASE_FIELD_CREATETIME_SORT_ORDER = 99
# 最后一次更新时间，触发器。
DATABASE_FIELD_LASTUPDATETIME_SERVER_DEFAULT = "CURRENT_TIMESTAMP ON UPDATE " "CURRENT_TIMESTAMP"
# 最后一次更新时间字段优先级
DATABASE_FIELD_LASTUPDATETIME_SORT_ORDER = 100
# 事务自动提交开关
DATABASE_SESSION_PARAM_AUTOCOMMIT = False
# 控制提交后实例是否过期。如果设置为 True，在提交后，实例的属性将被标记为过期，需要从数据库中刷新数据。
DATABASE_SESSION_PARAM_EXPIRE_ON_COMMIT = False
# 连接池中保留的连接数量
DATABASE_SESSION_PARAM_POOL_SIZE = 20
# 允许连接池在需要时超出 pool_size 指定数量的额外连接数
DATABASE_SESSION_PARAM_MAX_OVERFLOW = 10
# 使用连接之前先检查其是否有效开关
DATABASE_SESSION_PARAM_POOL_PRE_PING = True
# 会话未被初始化的报错信息
DATABASE_SESSION_NOT_INITIALIZED_EXCEPTION_PROMPT_MESSAGE = "数据库会话未被初始化。"

#######################################
# SCHEDULER
#######################################
# 检测间隔时间(秒)
SCHEDULER_DETECTION_INTERVAL_SECOND = 1

#######################################
# LARK
#######################################
# 飞书首次验证的类型
LARK_URL_VERIFICATION = "url_verification"
# 审批进行中状态
LARK_CALLBACK_APPROVAL_TASK_STATUS = "PENDING"
# 检查节点名称
LARK_CHECK_NODE_NAME = "check_node"
# 审批任务进行中状态
LARK_CHECK_NODE_TASK_STATUS = "PENDING"
# 执行节点名称
LARK_EXECUTE_NODE_NAME = "execute_node"
# 审批任务进行中状态
LARK_EXECUTE_NODE_TASK_STATUS = "PENDING"
# 工单 ID 分隔符
LARK_TICKET_ID_DELIMITER = "|"
# 检查成功默认文案
LARK_CHECK_SUCCESS_DEFAULT_COMMENT = "检查成功。"
# 检查失败默认文案
LARK_CHECK_FAILURE_DEFAULT_COMMENT = "检查失败。"
# 执行成功默认文案
LARK_EXECUTE_SUCCESS_DEFAULT_COMMENT = "执行成功。"
# 执行失败默认文案
LARK_EXECUTE_FAILURE_DEFAULT_COMMENT = "执行失败。"
