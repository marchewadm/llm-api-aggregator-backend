import uuid

from typing import Annotated
from datetime import timedelta, datetime, UTC
from cryptography.fernet import Fernet

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import jwt, JWTError

from src.shared.utils.hash import hash_util
from src.shared.utils.passphrase import passphrase_util
from src.shared.service.base import BaseService

from src.user.repository import UserRepository

from src.core.config import settings

from .schemas import (
    AuthCurrentUser,
    AuthRegisterRequest,
    AuthRegisterResponse,
    AuthLoginResponse,
)


class AuthService(BaseService[UserRepository]):
    """
    Service for auth related operations.
    """

    _oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/login")

    def __init__(
        self, repository: UserRepository = Depends(UserRepository)
    ) -> None:
        """
        Initializes the service with the repository.

        Args:
            repository (UserRepository): The repository to use for user operations.

        Returns:
            None
        """

        super().__init__(repository)

    @staticmethod
    def _create_access_token(user_id: int) -> str:
        """
        Creates an access token for a user.

        Args:
            user_id (int): The user's ID.

        Returns:
            str: The access token.
        """

        encode = {"sub": str(user_id), "uuid": str(uuid.uuid4())}
        expires = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES
        )
        encode.update({"exp": expires})

        return jwt.encode(
            encode, settings.JWT_AUTH_SECRET_KEY, settings.ALGORITHM
        )

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(_oauth2_bearer)]
    ) -> AuthCurrentUser:
        """
        Retrieves the current user from the token.

        Args:
            token (str): The user's token.

        Returns:
            UserCurrent: The current user containing the email and user ID.

        Raises:
            HTTPException: Raised with a 401 status code if the user cannot be authenticated or the token has expired.
        """

        try:
            payload = jwt.decode(
                token, settings.JWT_AUTH_SECRET_KEY, settings.ALGORITHM
            )
            user_id: str = payload.get("sub")
            redis_uuid: str = payload.get("uuid")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not authenticate user.",
                )
            return AuthCurrentUser(user_id=int(user_id), uuid=redis_uuid)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your session has expired. Please log in again.",
            )

    def create(self, payload: AuthRegisterRequest) -> AuthRegisterResponse:
        """
        Creates a user.

        Args:
            payload (AuthRegisterRequest): The user's email, name and password.

        Returns:
            AuthRegisterResponse: A message telling the user to check their email.
                Message can be customized, but defaults to the one in the schema.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["id"], "email", payload.email
        )

        if not user:
            self.repository.create(payload.model_dump(exclude={"password_2"}))
        return AuthRegisterResponse()

    def get_authenticated(
        self, payload: OAuth2PasswordRequestForm
    ) -> AuthLoginResponse:
        """
        Authenticates a user.

        Args:
            payload (OAuth2PasswordRequestForm): The user's email and password.

        Raises:
            HTTPException: Raised with a 401 status code if the user does not exist or the password is incorrect.

        Returns:
            AuthLoginResponse: The access token and token type.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["id", "password"], "email", payload.username
        )

        if not user or not hash_util.verify_hash(
            payload.password, user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your email or password is incorrect. Please try again.",
            )

        token = self._create_access_token(user.id)
        return AuthLoginResponse(access_token=token, token_type="bearer")

    def get_fernet_key(self, user_id: int, passphrase: str) -> Fernet:
        """
        Verify the user's passphrase and generate a Fernet key.

        Args:
            user_id (int): The user's ID.
            passphrase (str): The user's passphrase.

        Raises:
            HTTPException: Raised with a 400 status code if the passphrase is incorrect.

        Returns:
            Fernet: The Fernet key.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["passphrase", "passphrase_salt"], "id", user_id
        )

        if not hash_util.verify_hash(passphrase, user.passphrase):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please check your passphrase and try again.",
            )

        fernet_key = passphrase_util.generate_fernet_key(
            passphrase.encode(),
            passphrase_util.convert_hex_to_bytes(user.passphrase_salt),
        )
        return fernet_key
