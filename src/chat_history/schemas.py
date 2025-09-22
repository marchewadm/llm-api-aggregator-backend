from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field, PastDatetime, field_serializer

from src.shared.enums import RoleEnum, AiModelEnum


class ChatHistoryInDb(BaseModel):
    ai_model: AiModelEnum
    role: RoleEnum
    room_uuid: UUID
    message: str
    image_url: Annotated[str | None, Field(default=None)]
    api_provider_id: int
    custom_instructions: str


class ChatHistoryMessage(BaseModel):
    message: str
    image_url: Annotated[
        str | None, Field(serialization_alias="imageUrl", default=None)
    ]
    role: RoleEnum
    api_provider_id: Annotated[
        int | None, Field(serialization_alias="apiProviderId", default=None)
    ]
    sent_at: Annotated[PastDatetime, Field(serialization_alias="sentAt")]


class ChatHistoryResponse(BaseModel):
    room_uuid: Annotated[UUID, Field(serialization_alias="roomUuid")]
    ai_model: Annotated[AiModelEnum, Field(serialization_alias="aiModel")]
    custom_instructions: Annotated[
        str, Field(serialization_alias="customInstructions")
    ]
    messages: list[ChatHistoryMessage]

    @field_serializer("messages")
    def serialize_messages_ascending(self, messages: list[ChatHistoryMessage]):
        """
        Sort the messages by 'sent_at' date in ascending order.
        """

        messages.sort(key=lambda messages: messages.sent_at)
        return messages
