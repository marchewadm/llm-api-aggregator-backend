from abc import ABC, abstractmethod

from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException, status

from src.repositories.base import BaseRepository


class BaseService[T: BaseRepository](ABC):
    """
    Base abstract class for services.

    This class enforces the use of an instance of a base repository for operations.
    All services should inherit from this class.

    Contains some already implemented methods that can be used by child classes.
    """

    def __init__(self, repository: T) -> None:
        """
        Initialize the service with a repository.

        Args:
            repository (T): The repository to use for operations.

        Returns:
            None
        """

        self.repository = repository

    @abstractmethod
    def create(self, payload) -> None:
        """
        Create new entity and store it in the database.

        Args:
            payload: The data to create the entity with.

        Raises:
            TypeError: This method should be implemented in the child class.

        Returns:
            None
        """

        pass

    def get_one_by_id(self, entity_id: int):
        """
        Get an entity by its ID.

        Args:
            entity_id (int): The ID of the entity to retrieve.

        Raises:
            HTTPException: Raised with status code 404 if the entity is not found.
        """

        try:
            return self.repository.get_one_by_id(entity_id)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entity with ID {entity_id} not found",
            )

    def delete_by_id(self, entity_id: int) -> None:
        """
        Delete an entity by its ID.

        Args:
            entity_id (int): The ID of the entity to delete.

        Raises:
            HTTPException: Raised with status code 404 if the entity is not found.

        Returns:
            None
        """

        try:
            self.repository.delete_by_id(entity_id)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not delete entity with ID {entity_id}. Entity not found.",
            )
