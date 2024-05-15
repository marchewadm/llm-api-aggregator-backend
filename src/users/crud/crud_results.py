from dataclasses import dataclass


@dataclass
class UpdateUserPasswordResult:
    success: bool
    message: str
