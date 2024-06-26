from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    email: EmailStr


class UserProfileResponse(UserBase):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    avatar: Optional[str] = None
    passphrase: Optional[SecretStr] = None
