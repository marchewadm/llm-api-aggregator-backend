from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
    ValidationInfo,
)


class UserBase(BaseModel):
    email: EmailStr


class UserUpdatePasswordRequest(BaseModel):
    current_password: Annotated[
        SecretStr, Field(min_length=8, validation_alias="currentPassword")
    ]
    new_password: Annotated[
        SecretStr, Field(min_length=8, validation_alias="newPassword")
    ]
    new_password_2: Annotated[
        SecretStr, Field(min_length=8, validation_alias="newPassword2")
    ]

    @field_validator("new_password_2")
    @classmethod
    def validate_password(
        cls, value: SecretStr, info: ValidationInfo
    ) -> SecretStr:
        if (
            "new_password" in info.data
            and value.get_secret_value()
            != info.data["new_password"].get_secret_value()
        ):
            raise ValueError("Passwords do not match")
        if (
            "current_password" in info.data
            and value.get_secret_value()
            == info.data["current_password"].get_secret_value()
        ):
            raise ValueError(
                "New password cannot be the same as the old password"
            )
        return value


class UserUpdateProfileRequest(BaseModel):
    name: Annotated[
        str | None, Field(min_length=1, max_length=50, default=None)
    ]
    email: EmailStr | None = None
    avatar: str | None = None


class UserProfileResponse(UserBase):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    avatar: Optional[str] = None
    is_passphrase: Annotated[bool, Field(serialization_alias="isPassphrase")]


class UserUploadAvatarResponse(BaseModel):
    avatar: str


class UserUpdatePasswordResponse(BaseModel):
    message: str = (
        "Password updated successfully. Now you can log in with your new password."
    )


class UserUpdateProfileResponse(BaseModel):
    message: str
    name: Annotated[
        str | None, Field(min_length=1, max_length=50, default=None)
    ]
    email: EmailStr | None = None
    avatar: str | None = None


class UserUpdatePassphraseResponse(BaseModel):
    passphrase: str
