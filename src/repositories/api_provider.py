from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.database.core import get_db

from src.models.api_provider import ApiProvider

from .base import BaseRepository


class ApiProviderRepository(BaseRepository[ApiProvider]):
    """
    Repository for api provider database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, ApiProvider)

    def get_one_by_name(self, lowercase_name: str) -> ApiProvider | None:
        """
        Get the API provider by name.

        Args:
            lowercase_name (str): The name of the provider in lowercase.

        Returns:
            ApiProvider | None: The API provider object if found, None otherwise.
        """

        return self.db.scalar(
            select(self.model)
            .options(load_only(self.model.name, self.model.lowercase_name))
            .where(self.model.lowercase_name == lowercase_name)
        )

    def get_all(self) -> Sequence[ApiProvider]:
        """
        Get all API providers.

        Returns:
            Sequence[ApiProvider]: A sequence of API provider objects containing the name of the provider.
        """

        return self.db.scalars(
            select(self.model).options(load_only(self.model.name))
        ).all()
