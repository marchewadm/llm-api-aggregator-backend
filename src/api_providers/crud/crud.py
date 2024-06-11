from sqlalchemy.orm import Session

from src.database.models import ApiKey


def get_user_api_providers(db: Session, user_id: int) -> list[str]:
    """
    Retrieves all API providers associated with the user from the database based on the user's ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        list[str]: A list of API providers.
    """

    api_providers = (
        db.query(ApiKey.api_provider)
        .filter(ApiKey.user_id == user_id)  # noqa
        .order_by(ApiKey.id.asc())
        .all()
    )

    return [api_provider[0] for api_provider in api_providers]
