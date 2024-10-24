import uuid
import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

from src.chat_room.models import ChatRoom
from src.api_provider.models import ApiProvider

from src.shared.enums import RoleEnum, AiModelEnum


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_uuid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.room_uuid")
    )
    api_provider_id: Mapped[int] = mapped_column(ForeignKey("api_providers.id"))
    role: Mapped[RoleEnum]
    ai_model: Mapped[AiModelEnum]
    custom_instructions: Mapped[str]
    message: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chat_room: Mapped["ChatRoom"] = relationship(back_populates="chat_history")
    api_provider: Mapped["ApiProvider"] = relationship()
