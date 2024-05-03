from ..database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    text,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_password_reset_requested = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP, server_default=text("now()"), onupdate=text("now()")
    )

    api_keys = relationship("ApiKey", back_populates="user")


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="api_keys")
