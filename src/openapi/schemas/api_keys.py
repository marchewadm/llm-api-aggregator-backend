from pydantic import RootModel, BaseModel
from typing import List

from src.api_keys.schemas.schemas import ApiKeySchema


class GetApiKeysResponse(RootModel):
    """
    Schema for the response body of the GET /api-keys endpoint.

    Attributes:
        - root (List[ApiKeySchema]): A list of API keys.
    """

    root: List[ApiKeySchema]


class UpdateApiKeysResponse(BaseModel):
    """
    Schema for the response body of the PATCH /api-keys/update endpoint.

    Attributes:
        - message (str): A message indicating the result of the operation.
    """

    message: str
