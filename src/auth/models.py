import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.core import Base


class User(Base):
    # TODO: instead of creating a column named "is_passphrase", just create a function that checks if passphrase != null

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    avatar: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str]
    is_password_reset_requested: Mapped[bool] = mapped_column(default=False)
    passphrase: Mapped[Optional[str]]
    passphrase_salt: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    api_keys = relationship("ApiKey", back_populates="user")
