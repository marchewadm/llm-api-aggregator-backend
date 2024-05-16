from dataclasses import dataclass


@dataclass
class UpdateUserPasswordResult:
    is_success: bool
    message: str
    status_code: int = 200
