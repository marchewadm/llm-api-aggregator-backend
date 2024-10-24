from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field

from src.shared.enums import RoleEnum, AiModelEnum


class ChatHistoryCompletionMessage(BaseModel):
    message: str
    role: RoleEnum


class ChatHistoryCompletionRequest(BaseModel):
    room_uuid: Annotated[
        UUID | None, Field(validation_alias="roomUuid", default=None)
    ]
    api_provider_id: Annotated[int, Field(validation_alias="apiProviderId")]
    ai_model: Annotated[AiModelEnum, Field(validation_alias="aiModel")]
    custom_instructions: Annotated[
        str | None,
        Field(
            validation_alias="customInstructions",
            default="You are a helpful assistant.",
        ),
    ]
    messages: list[ChatHistoryCompletionMessage]


class ChatHistoryCompletionResponse(BaseModel):
    message: str
    room_uuid: Annotated[UUID, Field(serialization_alias="roomUuid")]
    api_provider_id: Annotated[int, Field(serialization_alias="apiProviderId")]
