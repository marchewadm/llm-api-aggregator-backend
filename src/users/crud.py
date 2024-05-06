from sqlalchemy.orm import Session

from src.auth.utils import bcrypt_context

from .models import User
from .schemas import UserCreate, UserLogin


def create_user(db: Session, user: UserCreate):
    """Inserts a new user into the database with a hashed password."""

    new_user = User(
        name=user.name,
        email=user.email,
        password=bcrypt_context.hash(user.password),
    )

    db.add(new_user)
    db.commit()

    return new_user


def get_user_by_email(db: Session, email: str):
    """Retrieves a user's email, password and is_verified email status from the database."""

    user = (
        db.query(User)
        .with_entities(User.email, User.password, User.is_verified, User.id)
        .filter(User.email == email)  # noqa
        .first()
    )

    return user
