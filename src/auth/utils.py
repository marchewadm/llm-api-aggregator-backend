from datetime import timedelta, datetime, UTC

from jose import jwt

from src.config import settings


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
