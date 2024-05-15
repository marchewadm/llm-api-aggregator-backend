from typing import Annotated, Optional
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ValidationInfo,
    ConfigDict,
    Field,
)


class ApiKeyBase(BaseModel):
    key: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: Annotated[str, Field(min_length=1)]
    password: Annotated[str, Field(min_length=8)]
    password2: Annotated[str, Field(min_length=8)]

    @field_validator("password2")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLogin(UserBase):
    password: Annotated[str, Field(min_length=8)]


class UserUpdatePassword(BaseModel):
    old_password: Annotated[
        str, Field(min_length=8, validation_alias="currentPassword")
    ]
    password: Annotated[
        str, Field(min_length=8, validation_alias="newPassword")
    ]
    password2: Annotated[
        str, Field(min_length=8, validation_alias="newPassword2")
    ]

    @field_validator("password2")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        if "old_password" in info.data and v == info.data["old_password"]:
            raise ValueError(
                "New password cannot be the same as the old password"
            )
        return v


class UserUpdateProfile(BaseModel):
    avatar: Optional[str] = None
    name: Optional[Annotated[str, Field(min_length=1)]] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    api_keys: list[ApiKey] = []


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    avatar: str | None = None
