from datetime import timedelta, datetime, UTC
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from .utils import bcrypt_context, oauth2_bearer
from src.constants import JWT_AUTH_SECRET_KEY, ALGORITHM
from src.database.dependencies import db_dependency
from src.users.crud.crud import get_user_by_email
from src.exceptions import NotAuthenticatedException


def authenticate_user(email: str, password: str, db: db_dependency):
    """Authenticates a user by their email and password."""

    user = get_user_by_email(db, email)

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    # TODO: Uncomment the following lines after email verification is implemented
    # if not user.is_verified:
    #     return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    """Creates an access token for a user."""

    encode = {"sub": email, "id": user_id}
    expires = datetime.now(UTC) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, JWT_AUTH_SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """Retrieves the current user from the token."""

    try:
        payload = jwt.decode(token, JWT_AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            raise NotAuthenticatedException(
                message="Could not authenticate user."
            )

        return {"email": email, "id": user_id}
    except JWTError:
        raise NotAuthenticatedException(
            message="Your session has expired. Please log in again."
        )
