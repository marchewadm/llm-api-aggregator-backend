from sqlalchemy.orm import Session, load_only

from .models import User
from .schemas import (
    UserCreate,
    UserLogin,
    UserUpdatePassword,
    UserUpdateProfile,
)
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


def get_desired_fields_by_user_id(
    db: Session, user_id: int, desired_fields: list[str]
):
    """
    Retrieves the desired fields of a user from the database based on their ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.
        desired_fields (list[str]): The desired fields to retrieve from the database.

    Returns:
        User: The user object containing the requested fields.

    TODO: make desired_fields a list of User fields instead of strings.
    """

    fields = [getattr(User, desired_field) for desired_field in desired_fields]
    user = (
        db.query(User)
        .options(load_only(*fields))
        .filter(User.id == user_id)  # noqa
        .first()
    )

    return user


def update_user_password(
    db: Session, user_id: int, user_data: UserUpdatePassword
):
    """Updates a user's password in the database by their ID."""

    user = get_desired_fields_by_user_id(db, user_id, ["password"])

    if not user:
        return False
    if not bcrypt_context.verify(user_data.old_password, user.password):
        return False

    user.password = bcrypt_context.hash(user_data.password)

    db.commit()
    return user


def update_user_profile(
    db: Session, user_id: int, user_data: UserUpdateProfile
):
    """Updates a user's profile in the database by their ID."""

    user = get_desired_fields_by_user_id(
        db, user_id, ["name", "email", "avatar"]
    )

    if not user:
        return False

    is_updated = False
    for field, new_value in user_data.dict().items():
        current_value = getattr(user, field)
        if new_value is not None and new_value != current_value:
            setattr(user, field, new_value)
            is_updated = True

    if is_updated:
        db.commit()
    return is_updated
