from sqlalchemy.exc import IntegrityError

from fastapi import Depends, HTTPException, status, UploadFile

from src.shared.utils.hash import hash_util
from src.shared.utils.passphrase import passphrase_util
from src.shared.service.base import BaseService

from src.s3.dependencies import S3ServiceDependency

from .repository import UserRepository
from .schemas import (
    UserUpdatePasswordRequest,
    UserUpdateProfileRequest,
    UserProfileResponse,
    UserUpdatePasswordResponse,
    UserUpdateProfileResponse,
    UserUpdatePassphraseResponse,
)


class UserService(BaseService[UserRepository]):
    """
    Service for user related operations.
    """

    def __init__(
        self,
        s3_service: S3ServiceDependency,
        repository: UserRepository = Depends(UserRepository),
    ) -> None:
        """
        Initializes the service with the repository.

        Args:
            repository (UserRepository): The repository to use for user operations.

        Returns:
            None
        """

        super().__init__(repository)
        self.s3_service = s3_service

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
        self, user_id: int, payload: UserUpdatePasswordRequest
    ) -> UserUpdatePasswordResponse:
        """
        Update a user's password by ID.

        Args:
            user_id (int): The ID of the user to update.
            payload (UserUpdatePasswordRequest): The payload containing the current and new password.

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

    async def update_user_profile(
        self,
        user_id: int,
        payload: UserUpdateProfileRequest,
        avatar: UploadFile | None,
    ) -> UserUpdateProfileResponse:
        """
        Update a user's profile by ID.

        """

        user = self.repository.get_one_with_selected_attributes_by_condition(
            ["name", "email", "avatar"], "id", user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        updated_fields = {}
        is_updated = False

        if avatar:
            if user.avatar:
                self.s3_service.delete_file(user.avatar)

            updated_fields["avatar"] = await self.s3_service.upload_file(
                avatar, "avatars"
            )
            is_updated = True

        if payload.name and payload.name != user.name:
            updated_fields["name"] = payload.name
            is_updated = True

        if payload.email and payload.email != user.email:
            updated_fields["email"] = payload.email
            is_updated = True

        if is_updated:
            try:
                self.repository.update_profile_by_id(user_id, updated_fields)
            except IntegrityError:
                # Pass the exception to prevent leaking sensitive information like already existing email
                pass
            updated_fields["message"] = (
                "We've sent you a verification email. Please check your inbox. "
                if "email" in updated_fields
                else "Profile updated successfully."
            )
        else:
            updated_fields["message"] = (
                "Your profile is up to date. No changes were made."
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
