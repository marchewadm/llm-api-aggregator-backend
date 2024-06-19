from sqlalchemy.orm import Session, load_only

from src.database.models import User, ApiKey
from src.users.schemas.schemas import (
    UserCreate,
    UserUpdatePassword,
    UserUpdateProfile,
)
from .crud_results import (
    CreateUserResult,
    UpdateUserPasswordResult,
    UpdateUserProfileResult,
    UpdateUserPassphraseResult,
)
from src.auth.utils import bcrypt_context
from ..utils.utils import generate_salt, generate_strong_passphrase
from src.common.utils import convert_bytes_to_hex


def create_user(db: Session, user: UserCreate) -> CreateUserResult:
    """
    Inserts a new user into the database with a hashed password.
    Due to security reasons, the return value is always the same message, regardless of the outcome.
    I don't want to leak information about whether the email is already taken or not.

    TODO: Implement a rate limiter for sending verification emails (e.g. 1 email per 10 minutes).
    TODO: Implement a verification email system. If the email is already taken, the user with that email should be
    TODO: notified that someone tried to register with their email.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to insert into the database.

    Returns:
        CreateUserResult: The result of the operation containing a message.
    """

    is_email_taken = (
        db.query(User)
        .options(load_only(User.id))
        .filter(User.email == user.email)  # noqa
        .first()
    )

    if not is_email_taken:
        new_user = User(
            name=user.name,
            email=user.email,
            password=bcrypt_context.hash(user.password),
        )
        db.add(new_user)
        db.commit()
    return CreateUserResult(
        message="We've sent you a verification email. Please check your inbox."
        " If you don't see it, check your spam folder or try again later."
    )


def get_user_by_email(db: Session, email: str):
    """
    Retrieves a user's email, password and is_verified email status from the database.

    Args:
        db (Session): The database session.
        email (str): The user's email.

    Returns:
        User: The user object containing the requested fields.
    """

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


def get_user_passphrase(db: Session, user_id: int):
    """"""

    user = get_desired_fields_by_user_id(
        db, user_id, ["passphrase", "passphrase_salt"]
    )
    return user


def update_user_password(
    db: Session, user_id: int, user_data: UserUpdatePassword
) -> UpdateUserPasswordResult:
    """
    Updates a user's password in the database by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.
        user_data (UserUpdatePassword): The user data containing the old and new passwords.

    Returns:
        UpdateUserPasswordResult: The result of the operation containing
        is_success flag, a message and an optional status code (default is 200).
    """

    user = get_desired_fields_by_user_id(db, user_id, ["password"])

    if not user:
        return UpdateUserPasswordResult(
            is_success=False,
            message="Could not authenticate user.",
            status_code=404,
        )
    if not bcrypt_context.verify(user_data.old_password, user.password):
        return UpdateUserPasswordResult(
            is_success=False,
            message="Please check your credentials and try again.",
            status_code=400,
        )

    user.password = bcrypt_context.hash(user_data.password)
    db.commit()
    return UpdateUserPasswordResult(
        is_success=True,
        message="Password updated successfully. Now you can log in with your new password.",
    )


def update_user_passphrase(
    db: Session, user_id: int
) -> UpdateUserPassphraseResult:
    """
    Updates a user's passphrase in the database by their ID.
    All API keys associated with the user are deleted.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        UpdateUserPassphraseResult: The result of the operation containing the generated passphrase.
    """

    user = get_desired_fields_by_user_id(
        db, user_id, ["passphrase", "passphrase_salt", "is_passphrase"]
    )
    passphrase = generate_strong_passphrase()
    salt = convert_bytes_to_hex(generate_salt())

    user.passphrase = bcrypt_context.hash(passphrase)
    user.passphrase_salt = salt

    if not user.is_passphrase:
        user.is_passphrase = True

    db.query(ApiKey).filter(ApiKey.user_id == user_id).delete()  # noqa

    db.commit()
    return UpdateUserPassphraseResult(passphrase=passphrase)


def update_user_profile(
    db: Session, user_id: int, user_data: UserUpdateProfile
) -> UpdateUserProfileResult:
    """
    Updates a user's profile in the database by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.
        user_data (UserUpdateProfile): The user data containing optional fields to update: name, email and avatar.

    Returns:
        UpdateUserProfileResult: The result of the operation containing a message and the updated fields.

    TODO: if the user tries to update their email, send a verification email to the new email.
    """

    user = get_desired_fields_by_user_id(
        db, user_id, ["name", "email", "avatar"]
    )

    is_updated: bool = False
    fields_to_update: dict = {}

    for field, new_value in user_data.dict().items():
        current_value = getattr(user, field)
        if new_value is not None and new_value != current_value:
            setattr(user, field, new_value)
            is_updated = True
            fields_to_update.update({field: new_value})

    if is_updated:
        db.commit()
        if "email" in fields_to_update:
            fields_to_update.update(
                {
                    "message": "We've sent you a verification email. Please check your inbox."
                    " If you don't see it, check your spam folder or try updating your email later."
                }
            )
        else:
            fields_to_update.update(
                {"message": "Profile updated successfully."}
            )
    else:
        fields_to_update.update(
            {"message": "Your profile is up to date. No changes were made."}
        )
    return UpdateUserProfileResult(**fields_to_update)
