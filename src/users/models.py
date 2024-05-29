from typing import Optional
from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

from src.api_keys.models import ApiKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    avatar: Mapped[Optional[str]]
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_password_reset_requested: Mapped[bool] = mapped_column(default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    api_keys = relationship("ApiKey", back_populates="user")
