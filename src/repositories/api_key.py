from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload

from fastapi import Depends

from src.database.core import get_db

from src.models.api_key import ApiKey

from .base import BaseRepository


class ApiKeyRepository(BaseRepository[ApiKey]):
    """
    Repository for api key database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, ApiKey)

    def get_all_by_user_id(self, user_id: int) -> Sequence[ApiKey]:
        """
        Get all user's API keys by user ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            Sequence[ApiKey]: A sequence of API key objects containing the key, API provider name and lowercase name.
        """

        return self.db.scalars(
            select(self.model)
            .options(joinedload(self.model.api_provider))
            .where(self.model.user_id == user_id)
        ).all()

    def delete_all_by_user_id(self, user_id: int) -> None:
        """
        Delete all user's API keys by user ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """

        self.db.execute(delete(self.model).where(self.model.user_id == user_id))
        self.db.commit()
