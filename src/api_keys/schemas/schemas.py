from typing import Annotated
from pydantic import BaseModel, Field


class ApiKeySchema(BaseModel):
    key: Annotated[str, Field(min_length=1)]
    ai_model: Annotated[
        str, Field(min_length=1, max_length=15, validation_alias="aiModel")
    ]
