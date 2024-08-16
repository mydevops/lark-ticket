"""配置表模块."""

from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import exists
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base
from src.db.base import HasCreateTimeMixin
from src.db.base import HasIdMixin
from src.db.base import HasLastUpdateTimeMixin
from src.lib import schema


class ConfigModel(HasIdMixin, HasCreateTimeMixin, HasLastUpdateTimeMixin, Base):
    """配置表定义."""

    __tablename__ = "tb_config"

    approval_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="审批定义 code")
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=False, comment="审批配置名称")
    check: Mapped[schema.CheckConfig] = mapped_column(JSON, nullable=False, comment="检查节点配置")
    execute: Mapped[schema.ExecuteConfig] = mapped_column(JSON, nullable=False, comment="执行节点配置")
    field: Mapped[schema.FieldConfig] = mapped_column(JSON, nullable=False, comment="外部字段配置")
    relation: Mapped[schema.RelationConfig] = mapped_column(JSON, nullable=False, comment="关联字段配置")

    @classmethod
    async def get(cls, session: AsyncSession, approval_code: str) -> schema.Config:
        """根据审批定义 code 检索配置.

        Args:
            session: 数据库会话.
            approval_code: 审批定义 code.

        Returns:
            schema.Config: 指定审批代码的配置.
        """
        entry = await session.scalar(select(cls).where(cls.approval_code == approval_code))
        return schema.Config(
            approval_code=entry.approval_code,
            name=entry.name,
            check=entry.check,
            execute=entry.execute,
            field=entry.field,
            relation=entry.relation,
        )

    @classmethod
    async def exists(cls, session: AsyncSession, approval_code: str) -> bool:
        """检查指定的审批定义 code 是否存在.

        Args:
            session: 数据库会话.
            approval_code: 审批定义 code.

        Returns:
            True: 存在
            False: 不存在
        """
        return await session.scalar(exists().where(cls.approval_code == approval_code).select())

    def __repr__(self) -> str:
        """打印时的字符串格式."""
        return (
            f"ConfigModel(id={self.id!r} approval_code={self.approval_code!r} name={self.name!r} "
            f"check={self.check!r} execute={self.execute!r} field={self.field!r} relation={self.relation!r})"
        )
