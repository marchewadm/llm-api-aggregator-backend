from fastapi import Depends

from src.repositories.user import UserRepository

from .schemas import UserRegister, UserRegisterResponse


class UserService:
    """
    Service for user related operations.
    """

    def __init__(
        self, repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.repository = repository

    def create(self, payload: UserRegister) -> UserRegisterResponse:
        is_email_taken = self.repository.get_by_email(payload.email)

        if not is_email_taken:
            self.repository.create(payload)

        return UserRegisterResponse(
            message="We've sent you a verification email. Please check your inbox."
            " If you don't see it, check your spam folder or try again later."
        )
