from uuid import UUID
from typing import Literal, Optional

from pydantic import BaseModel

from src.shared.schemas.common import ChatHistoryInDb, ChatHistoryResponse


class OpenAiModel(BaseModel):
    ai_model: Literal[
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ]


class OpenAiRole(BaseModel):
    role: Literal["user", "assistant"]


class OpenAiChatCompletionMessage(OpenAiRole):
    content: str


class OpenAiChatCompletionRequest(OpenAiModel):
    room_uuid: Optional[UUID] = None
    custom_instructions: Optional[str] = "You are a helpful assistant."
    messages: list[OpenAiChatCompletionMessage]


class OpenAiChatCompletionResponse(BaseModel):
    room_uuid: UUID
    response_message: str


class OpenAiChatHistoryInDb(OpenAiModel, OpenAiRole, ChatHistoryInDb):
    custom_instructions: str


class OpenAiChatHistoryMessageObject(OpenAiRole, ChatHistoryResponse):
    pass


class OpenAiChatHistoryResponse(BaseModel):
    room_uuid: UUID
    messages: list[OpenAiChatHistoryMessageObject]
