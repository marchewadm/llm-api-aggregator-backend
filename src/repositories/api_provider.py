from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from fastapi import Depends

from src.database.core import get_db

from src.models.api_provider import ApiProvider
from src.schemas.api_provider import ApiProviderCreate


class ApiProviderRepository:
    """
    Repository for api provider database related operations.
    """

    def __init__(self, db: Session = Depends(get_db)) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        self.db = db
        self.model = ApiProvider

    def create(self, payload: ApiProviderCreate) -> None:
        """
        Create a new API provider in the database.

        Args:
            payload (ApiProviderCreate): API provider creation payload containing name of the provider.

        Returns:
            None
        """

        self.db.add(
            ApiProvider(
                name=payload.name,
                lowercase_name=payload.lowercase_name,
            )
        )
        self.db.commit()
        return

    def get_one(self, lowercase_name: str):
        """
        Get the API provider by name.

        Args:
            lowercase_name (str): The name of the provider in lowercase.

        Returns:
            ApiProvider: The API provider object containing the name of the provider.
        """

        return self.db.scalar(
            select(self.model)
            .options(load_only(self.model.name, self.model.lowercase_name))
            .where(self.model.lowercase_name == lowercase_name)
        )

    def get_many(self):
        """
        Get all API providers.

        Returns:
            pass
        """

        return self.db.scalars(
            select(self.model).options(load_only(self.model.name))
        ).all()
