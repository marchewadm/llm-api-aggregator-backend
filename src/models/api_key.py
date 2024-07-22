import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, UniqueConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

# Due to circular import error we need to use TYPE_CHECKING to avoid it.
# More info at: https://github.com/sqlalchemy/sqlalchemy/discussions/9576#discussioncomment-5510161
if TYPE_CHECKING:
    from .user import User
    from .api_provider import ApiProvider


class ApiKey(Base):
    __tablename__ = "api_keys"
    __table_args__ = (UniqueConstraint("api_provider_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    api_provider_id: Mapped[int] = mapped_column(ForeignKey("api_providers.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="api_keys")
    api_provider: Mapped["ApiProvider"] = relationship()
