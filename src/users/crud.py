from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate, UserLogin, UserUpdatePassword
from src.auth.utils import bcrypt_context


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


def get_user_by_id(db: Session, user_id: int):
    """Retrieves a user by their ID from the database."""

    user = db.query(User).filter(User.id == user_id).first()  # noqa
    return user


def update_user_password(
    db: Session, user_data: UserUpdatePassword, user_id: int
):
    """Updates a user's password in the database by their ID."""

    user = get_user_by_id(db, user_id)

    if not user:
        return False
    if not bcrypt_context.verify(user_data.old_password, user.password):
        return False

    user.password = bcrypt_context.hash(user_data.password)

    db.commit()

    return user
