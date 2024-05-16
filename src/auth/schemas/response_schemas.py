from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Schema for the response body of the POST /auth/signup endpoint.

    Attributes:
        - message (str): A message indicating the result of the operation.
    """

    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
