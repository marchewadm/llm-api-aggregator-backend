import uuid
import datetime

from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.chat_room.models import ChatRoom


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(50))
    room_uuid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.room_uuid")
    )
    message: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chat_room: Mapped["ChatRoom"] = relationship(back_populates="chat_history")

    __mapper_args__ = {
        "polymorphic_identity": "chat_history",
        "polymorphic_on": "type",
    }
