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

    def delete_by_id(self, entity_id: int) -> None:
        """
        Delete an entity from the database by its ID.

        Args:
            entity_id (int): The ID of the entity to delete from the database.

        Returns:
            None
        """

        self.db.delete(self.db.get_one(self.model, entity_id))
        self.db.commit()
