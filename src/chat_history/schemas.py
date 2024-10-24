from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field

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
    role: RoleEnum
    api_provider_id: Annotated[
        int | None, Field(serialization_alias="apiProviderId", default=None)
    ]


class ChatHistoryResponse(BaseModel):
    room_uuid: Annotated[UUID, Field(serialization_alias="roomUuid")]
    ai_model: Annotated[AiModelEnum, Field(serialization_alias="aiModel")]
    custom_instructions: Annotated[
        str, Field(serialization_alias="customInstructions")
    ]
    messages: list[ChatHistoryMessage]
