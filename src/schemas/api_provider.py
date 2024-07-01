from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic.json_schema import SkipJsonSchema


class ApiProvider(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[str, Field(min_length=1, max_length=50)]


class ApiProviderCreate(ApiProvider):
    model_config = ConfigDict(str_strip_whitespace=True)

    lowercase_name: SkipJsonSchema[str] = Field(default="", exclude=True)

    @model_validator(mode="after")
    def set_lowercase_name(self) -> Self:
        self.lowercase_name = self.name.lower()
        return self


class ApiProviderCreateResponse(BaseModel):
    message: str = "API provider created successfully."


class ApiProvidersResponse(BaseModel):
    api_providers: list[ApiProvider]
