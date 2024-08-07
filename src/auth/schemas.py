from typing import Annotated, Self

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from src.shared.utils.hash import hash_util


class AuthCurrentUser(BaseModel):
    user_id: int
    uuid: str


class AuthRegisterRequest(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(min_length=1, max_length=50)]
    password: Annotated[SecretStr | str, Field(min_length=8)]
    password_2: Annotated[SecretStr, Field(min_length=8)]

    @field_validator("password_2")
    @classmethod
    def validate_password(
        cls, value: SecretStr, info: ValidationInfo
    ) -> SecretStr:
        if (
            "password" in info.data
            and value.get_secret_value()
            != info.data["password"].get_secret_value()
        ):
            raise ValueError("Passwords do not match")
        return value

    @model_validator(mode="after")
    def hash_password(self) -> Self:
        self.password = hash_util.create_hash(self.password.get_secret_value())
        return self


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str


class AuthRegisterResponse(BaseModel):
    message: str = (
        "We've sent you a verification email. Please check your inbox."
        " If you don't see it, check your spam folder or try again later."
    )
