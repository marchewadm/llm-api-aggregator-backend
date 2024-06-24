from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.repositories.user import UserRepository
from src.utils import verify_hash

from .utils import create_access_token
from .schemas import (
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
)


class UserService:
    """
    Service for user related operations.
    """

    def __init__(
        self, repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.repository = repository

    def authenticate(
        self, payload: OAuth2PasswordRequestForm
    ) -> UserLoginResponse:
        user = self.repository.get_by_email(payload.username)

        if not user or not verify_hash(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your email or password is incorrect. Please try again.",
            )

        token = create_access_token(
            payload.username,
            user.id,
        )

        return UserLoginResponse(access_token=token, token_type="bearer")

    def create(self, payload: UserRegister) -> UserRegisterResponse:
        is_email_taken = self.repository.get_by_email(payload.email)

        if not is_email_taken:
            self.repository.create(payload)

        return UserRegisterResponse(
            message="We've sent you a verification email. Please check your inbox."
            " If you don't see it, check your spam folder or try again later."
        )
