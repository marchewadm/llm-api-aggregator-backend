from typing import Annotated, Self

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    ValidationInfo,
    Field,
    field_validator,
    model_validator,
)

from src.utils import bcrypt_context


class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: Annotated[SecretStr, Field(min_length=8)]


class UserRegister(UserBase):
    name: Annotated[str, Field(min_length=1)]
    password: Annotated[SecretStr | str, Field(min_length=8)]
    password_2: Annotated[SecretStr, Field(min_length=8)]

    @field_validator("password_2")  # noqa
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
        self.password = bcrypt_context.hash(self.password.get_secret_value())
        return self


class UserRegisterResponse(BaseModel):
    message: str
