from pydantic import RootModel, BaseModel
from typing import Dict


class GetApiKeysResponse(RootModel):
    """
    Schema for the response body of the GET /api-keys endpoint.

    Attributes:
        - root (Dict[str, str]): The user's API keys.
    """

    root: Dict[str, str]


class UpdateApiKeysResponse(BaseModel):
    """
    Schema for the response body of the PATCH /api-keys/update endpoint.

    Attributes:
        - message (str): A message indicating the result of the operation.
    """

    message: str
