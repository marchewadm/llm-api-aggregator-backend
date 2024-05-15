from typing import Optional
from pydantic import BaseModel, EmailStr


class GetUserProfileResponse(BaseModel):
    """
    Schema for the response body of the GET /user/profile endpoint.

    Attributes:
        - name (str): The user's name.
        - email (EmailStr): The user's email.
        - avatar (str | None): The user's avatar URL, if available.
    """

    name: str
    email: EmailStr
    avatar: str | None = None


class UpdateUserPasswordResponse(BaseModel):
    """
    Schema for the response body of the PATCH /user/update-password endpoint.

    Attributes:
        - message (str): A message indicating the result of the operation.
    """

    message: str


class UpdateUserProfileResponse(BaseModel):
    """
    Schema for the response body of the PATCH /user/update-profile endpoint.
    """

    pass
