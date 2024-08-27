from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only


class BaseRepository[T]:
    """
    Base repository for database related operations.

    All repositories should inherit from this class.
    """

    def __init__(self, db: Session, model: type[T]) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        self.db = db
        self.model = model

    def create(self, payload: dict) -> None:
        """
        Create a new record in the database.

        Args:
            payload (dict): Payload containing the data to be created.

        Returns:
            None
        """

        self.db.add(self.model(**payload))
        self.db.commit()

    def get_one_by_id(self, entity_id: int) -> T:
        """
        Get an entity from the database by its ID.

        Args:
            entity_id (int): The ID of the entity to retrieve from the database.

        Returns:
            T: The entity retrieved from the database.
        """

        return self.db.get_one(self.model, entity_id)

    def get_one_with_selected_attributes_by_condition(
        self,
        attributes_to_fetch: list[str],
        filter_attribute: str,
        filter_value: str | int,
    ) -> T:
        """
        Get selected attributes of an entity from the database based on a specific condition.

        Args:
            attributes_to_fetch (list[str]): The attributes to retrieve from the entity.
            filter_attribute (str): The attribute to use for filtering.
            filter_value (str | int): The value to compare the filter attribute against.

        Returns:
            T: The entity retrieved from the database.
        """

        selected_attributes = [
            getattr(self.model, attr) for attr in attributes_to_fetch
        ]
        filter_column = getattr(self.model, filter_attribute)

        return self.db.scalar(
            select(self.model)
            .options(load_only(*selected_attributes, raiseload=True))
            .where(filter_column == filter_value)
        )

    def delete_by_id(self, entity_id: int | UUID) -> None:
        """
        Delete an entity from the database by its ID.

        Args:
            entity_id (int | UUID): The ID of the entity to delete from the database.

        Returns:
            None
        """

        self.db.delete(self.db.get_one(self.model, entity_id))
        self.db.commit()


class BaseAiRepository[T](BaseRepository[T]):
    """
    Base abstract class for AI repositories.

    This class enforces the use of an instance of a base repository for operations.
    All AI repositories should inherit from this class.

    Contains some already implemented methods that can be used by child classes.
    """

    def __init__(self, db: Session, model: type[T]) -> None:
        """
        Initialize the AI repository with a database session.

        Args:
            db (Session): Database session.

        Returns:
            None
        """

        super().__init__(db, model)

    def get_chat_history_by_room_uuid(self, room_uuid: UUID) -> Sequence[T]:
        """
        Get the chat history for a specific chat room.

        Args:
            room_uuid (UUID): The UUID of the chat room.

        Returns:
            Sequence[T]: A sequence of chat history objects.
        """

        return self.db.scalars(
            select(self.model).where(self.model.room_uuid == room_uuid)
        ).all()
