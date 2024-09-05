from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field, PastDatetime

from src.shared.enums import RoleEnum, AiModelEnum


class ChatHistoryInDb(BaseModel):
    ai_model: AiModelEnum
    role: RoleEnum
    room_uuid: UUID
    message: str
    api_provider_id: int
    custom_instructions: str


class ChatHistoryMessage(BaseModel):
    message: str
    sent_at: Annotated[PastDatetime, Field(serialization_alias="sentAt")]
    role: RoleEnum


class ChatHistoryResponse(BaseModel):
    room_uuid: Annotated[UUID, Field(serialization_alias="roomUuid")]
    messages: list[ChatHistoryMessage]
