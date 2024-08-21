import uuid
from typing import Literal, Optional

from pydantic import BaseModel

from src.shared.schemas.common import ChatHistoryInDb


class OpenAiChatCompletionMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class OpenAiChatCompletionRequest(BaseModel):
    room_uuid: Optional[uuid.UUID] = None
    ai_model: Literal[
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ]
    custom_instructions: Optional[str] = "You are a helpful assistant."
    messages: list[OpenAiChatCompletionMessage]


class OpenAiChatCompletionResponse(BaseModel):
    room_uuid: uuid.UUID
    response_message: str


class OpenAiChatHistoryInDb(ChatHistoryInDb):
    role: Literal["user", "assistant"]
    ai_model: Literal[
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ]
    custom_instructions: str
