from fastapi import Depends, HTTPException, status

from src.utils.hash import hash_util
from src.repositories.user import UserRepository
from src.schemas.user import (
    UserUpdatePassword,
    UserProfileResponse,
    UserUpdatePasswordResponse,
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

        # user = self.repository.get_password_by_id(user_id)
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
