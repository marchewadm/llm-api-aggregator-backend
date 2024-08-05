from pydantic import BaseModel


class AiModelsResponse(BaseModel):
    ai_models: list[str]
