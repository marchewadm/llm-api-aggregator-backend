from typing import Annotated
from datetime import timedelta, datetime, UTC

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from src.config import settings

from .schemas import UserCurrent


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_access_token(email: str, user_id: int) -> str:
    """
    Creates an access token for a user.

    Args:
        email (str): The user's email.
        user_id (int): The user's ID.

    Returns:
        str: The access token.
    """

    encode = {"sub": email, "id": user_id}
    expires = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES
    )
    encode.update({"exp": expires})

    return jwt.encode(encode, settings.JWT_AUTH_SECRET_KEY, settings.ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> UserCurrent:
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
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not authenticate user.",
            )

        return UserCurrent(email=email, user_id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session has expired. Please log in again.",
        )
