import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

# Due to circular import error we need to use TYPE_CHECKING to avoid it.
# More info at: https://github.com/sqlalchemy/sqlalchemy/discussions/9576#discussioncomment-5510161
if TYPE_CHECKING:
    from .base_chat_history import BaseChatHistory


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    room_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    chat_history: Mapped[List["BaseChatHistory"]] = relationship(
        back_populates="chat_rooms"
    )
