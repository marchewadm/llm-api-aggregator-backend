from typing import Annotated
from pydantic import BaseModel, Field, AliasChoices


class ApiKeySchema(BaseModel):
    key: Annotated[str, Field(min_length=1)]
    api_provider: Annotated[
        str,
        Field(
            min_length=1,
            max_length=15,
            validation_alias=AliasChoices("api_provider", "apiProvider"),
            serialization_alias="apiProvider",
        ),
    ]
