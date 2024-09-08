from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PastDatetime


class ApiProvider(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Annotated[str, Field(min_length=1, max_length=50)]
    ai_models: list[str]


class ApiProviderResponse(ApiProvider):
    id: int
    lowercase_name: Annotated[str, Field(min_length=1, max_length=50)]
    ai_models: list[str]
    created_at: PastDatetime
    updated_at: PastDatetime


class ApiProvidersResponse(BaseModel):
    api_providers: list[ApiProvider]
