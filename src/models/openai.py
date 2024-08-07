from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_chat_history import BaseChatHistory


class OpenAiChatHistory(BaseChatHistory):
    __tablename__ = "openai_chat_histories"

    id: Mapped[int] = mapped_column(
        ForeignKey("chat_histories.id"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String(15))

    __mapper_args__ = {
        "polymorphic_identity": "openai_chat_histories",
    }
