import uuid

from pydantic import BaseModel


class AiModelsResponse(BaseModel):
    ai_models: list[str]


class ChatHistoryInDb(BaseModel):
    room_uuid: uuid.UUID
    message: str
