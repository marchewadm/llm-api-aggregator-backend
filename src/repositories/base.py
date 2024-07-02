from sqlalchemy.orm import Session


class BaseRepository[T]:
    """
    Base repository for database related operations.
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
