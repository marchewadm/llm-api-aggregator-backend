from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.models.base import ChatHistory


class OpenAiChatHistory(ChatHistory):
    __tablename__ = "openai_chat_history"

    id: Mapped[int] = mapped_column(
        ForeignKey("chat_history.id"), primary_key=True, autoincrement=True
    )
    role: Mapped[str] = mapped_column(String(15))
    ai_model: Mapped[str]
    custom_instructions: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "openai_chat_history",
    }
