from fastapi import Depends, HTTPException, status

from src.repositories.user import UserRepository
from src.schemas.user import UserProfileResponse


class UserService:
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

        self.repository = repository

    def get_user_profile(self, user_id: int) -> UserProfileResponse:
        """
        Get a user's profile by ID.

        Args:
            user_id (int): The ID of the user to get.

        Returns:
            UserProfileResponse: The user's profile response containing the user's email, name, avatar and passphrase.
        """

        user = self.repository.get_profile_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return UserProfileResponse(**user.__dict__)
