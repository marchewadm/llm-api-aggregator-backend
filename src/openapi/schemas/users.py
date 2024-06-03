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

    Attributes:
        - message (str): A message indicating the result of the operation.
        - name (str | None): The user's updated name, if available.
        - email (EmailStr | None): The user's updated email, if available.
        - avatar (str | None): The user's updated avatar URL, if available.
    """

    message: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
