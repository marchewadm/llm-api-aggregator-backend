from sqlalchemy.exc import IntegrityError

from fastapi import Depends, HTTPException, status

from src.utils.hash import hash_util
from src.utils.passphrase import passphrase_util

from src.repositories.user import UserRepository

from src.schemas.user import (
    UserUpdatePassword,
    UserUpdateProfile,
    UserProfileResponse,
    UserUpdatePasswordResponse,
    UserUpdateProfileResponse,
    UserUpdatePassphraseResponse,
)

from .base import BaseService


class UserService(BaseService[UserRepository]):
    """
    Service for user related operations.
    """

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

    def create(self, payload) -> None:
        """
        This method is implemented in AuthService, but not in UserService.
        """

        pass

    def get_profile(self, user_id: int) -> UserProfileResponse:
        """
        Get a user's profile by ID.

        Args:
            user_id (int): The ID of the user to get.

        Returns:
            UserProfileResponse: The user's profile response containing the user's email, name, avatar and passphrase.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["email", "name", "avatar", "passphrase"], "id", user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return UserProfileResponse(
            email=user.email,
            name=user.name,
            avatar=user.avatar,
            is_passphrase=True if user.passphrase else False,
        )

    def update_user_password(
        self, user_id: int, payload: UserUpdatePassword
    ) -> UserUpdatePasswordResponse:
        """
        Update a user's password by ID.

        Args:
            user_id (int): The ID of the user to update.
            payload (UserUpdatePassword): The payload containing the current and new password.

        Raises:
            HTTPException: Raised with status code 400 if the current password is incorrect.
            HTTPException: Raised with status code 404 if the user is not found.

        Returns:
            UserUpdatePasswordResponse: The response containing a message if the operation is successful.
                Message can be customized, but defaults to the one in the schema.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["password"], "id", user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        if not hash_util.verify_hash(
            payload.current_password.get_secret_value(), user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please check your credentials and try again.",
            )

        hashed_new_password = hash_util.create_hash(
            payload.new_password.get_secret_value()
        )

        self.repository.update_password_by_id(user_id, hashed_new_password)
        return UserUpdatePasswordResponse()

    def update_user_profile(
        self, user_id: int, payload: UserUpdateProfile
    ) -> UserUpdateProfileResponse:
        """
        Update a user's profile by ID.

        Args:
            user_id (int): The ID of the user to update.
            payload (UserUpdateProfile): The payload containing optional fields to update: name, email and avatar.

        Raises:
            HTTPException: Raised with status code 404 if the user is not found.

        Returns:
            UserUpdateProfileResponse: The response containing a message if the operation is successful or not.
                Also contains the updated name, email and avatar if available.
        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["name", "email", "avatar"], "id", user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        updated_fields: dict = {}
        is_updated: bool = False

        for field, new_value in payload.dict().items():
            current_value = getattr(user, field)
            if new_value is not None and new_value != current_value:
                is_updated = True
                updated_fields.update({field: new_value})

        if is_updated:
            try:
                self.repository.update_profile_by_id(user_id, updated_fields)
            except IntegrityError:
                # Pass the exception to prevent leaking sensitive information like already existing email
                pass
            finally:
                if "email" in updated_fields:
                    updated_fields.update(
                        {
                            "message": "We've sent you a verification email. Please check your inbox."
                            " If you don't see it, check your spam folder or try updating your email later."
                        }
                    )
                else:
                    updated_fields.update(
                        {"message": "Profile updated successfully."}
                    )
        else:
            updated_fields.update(
                {"message": "Your profile is up to date. No changes were made."}
            )
        return UserUpdateProfileResponse(**updated_fields)

    def update_user_passphrase(
        self, user_id: int
    ) -> UserUpdatePassphraseResponse:
        """
        Create a new passphrase and return it for the user.
        The passphrase is hashed and stored in the database with a salt. It can be used later for creating fernet keys.

        Args:
            user_id (int): The ID of the user to update.

        Returns:
            UserUpdatePassphraseResponse: The response containing the new passphrase.
        """

        passphrase = passphrase_util.generate_strong_passphrase()
        passphrase_salt = passphrase_util.convert_bytes_to_hex(
            passphrase_util.generate_salt()
        )
        hashed_passphrase = hash_util.create_hash(passphrase)

        self.repository.update_passphrase_by_id(
            user_id,
            {
                "passphrase": hashed_passphrase,
                "passphrase_salt": passphrase_salt,
            },
        )
        return UserUpdatePassphraseResponse(passphrase=passphrase)
