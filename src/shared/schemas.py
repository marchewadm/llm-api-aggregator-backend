from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from src.shared.enums import RoleEnum, AiModelEnum


class AiModelsResponse(BaseModel):
    ai_models: list[str]


class ChatHistoryCompletionMessage(BaseModel):
    message: str
    role: RoleEnum


class ChatHistoryCompletionRequest(BaseModel):
    room_uuid: Optional[UUID] = None
    api_provider_id: int
    ai_model: AiModelEnum
    custom_instructions: Optional[str] = "You are a helpful assistant."
    messages: list[ChatHistoryCompletionMessage]


class ChatHistoryCompletionResponse(BaseModel):
    room_uuid: UUID
    message: str
