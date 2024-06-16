from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateUserResult:
    message: str


@dataclass
class UpdateUserPasswordResult:
    is_success: bool
    message: str
    status_code: int = 200


@dataclass
class UpdateUserProfileResult:
    message: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None


@dataclass
class UpdateUserPassphraseResult:
    passphrase: str
