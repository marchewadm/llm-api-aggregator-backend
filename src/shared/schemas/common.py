from uuid import UUID

from pydantic import BaseModel, PastDatetime


class AiModelsResponse(BaseModel):
    ai_models: list[str]


class ChatHistoryInDb(BaseModel):
    room_uuid: UUID
    message: str


class ChatHistoryResponse(BaseModel):
    message: str
    sent_at: PastDatetime
