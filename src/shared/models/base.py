import uuid
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

# Due to circular import error we need to use TYPE_CHECKING to avoid it.
# More info at: https://github.com/sqlalchemy/sqlalchemy/discussions/9576#discussioncomment-5510161
if TYPE_CHECKING:
    from .chat_room import ChatRoom


class BaseChatHistory(Base):
    __tablename__ = "chat_histories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(50))
    room_uuid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.room_uuid")
    )
    message: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    room: Mapped["ChatRoom"] = relationship(back_populates="chat_histories")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "chat_histories",
    }
