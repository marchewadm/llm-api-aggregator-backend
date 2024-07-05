from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, computed_field, PastDatetime


class ApiProvider(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Annotated[str, Field(min_length=1, max_length=50)]


class ApiProviderCreate(ApiProvider):
    model_config = ConfigDict(str_strip_whitespace=True)

    @computed_field
    @property
    def lowercase_name(self) -> str:
        return self.name.lower()


class ApiProviderCreateResponse(BaseModel):
    message: str = "API provider created successfully."


class ApiProviderResponse(ApiProvider):
    id: int
    lowercase_name: Annotated[str, Field(min_length=1, max_length=50)]
    created_at: PastDatetime
    updated_at: PastDatetime


class ApiProvidersResponse(BaseModel):
    api_providers: list[ApiProvider]
