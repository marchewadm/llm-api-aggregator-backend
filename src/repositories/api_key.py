from typing import Sequence

from sqlalchemy import select, insert, update, delete, or_
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

    def create_bulk(self, api_keys: list[dict]) -> None:
        """
        Create multiple API keys in the database.

        Args:
            api_keys (list[dict]): A list of API key dictionaries.

        Returns:
            None
        """

        self.db.execute(insert(self.model).values(api_keys))
        self.db.commit()

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

    def update_bulk_by_user_id(
        self, user_id: int, api_keys: list[dict]
    ) -> None:
        """
        Update multiple API keys in the database by user ID.

        Args:
            user_id (int): The user's ID.
            api_keys (list[dict]): A list of API key dictionaries.

        Returns:
            None
        """

        self.db.connection().execute(
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(api_keys)
        )
        self.db.commit()

    def delete_selected_by_user_id(
        self, user_id: int, api_keys: list[dict]
    ) -> None:
        """
        Delete selected API keys by user ID.

        Args:
            user_id (int): The user's ID.
            api_keys (list[dict]): A list of API key dictionaries to delete.

        Returns:
            None
        """

        conditions = [
            self.model.api_provider_id == api_key["api_provider_id"]
            for api_key in api_keys
        ]

        stmt = (
            delete(self.model)
            .where(self.model.user_id == user_id)
            .where(or_(*conditions))
        )

        self.db.execute(stmt)
        self.db.commit()

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
