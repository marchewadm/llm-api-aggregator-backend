from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)

from src.core.database import get_db
from src.api_provider.models import ApiProvider


def create_api_providers() -> None:
    """
    Initializes the database with predefined API providers.

    This function inserts a set of predefined API providers (e.g., OpenAI) into the database. Each provider is
    associated with a list of AI models it supports. It is intended to be run only once during the application's
    first-time setup to ensure that the necessary data exists in the database.

    IMPORTANT: Before running this function, ensure that:
    1. The database is initialized.
    2. The necessary tables are created by executing the migration command:
       `alembic upgrade head`.

    After running this function, the API providers will be available in the database.

    Returns:
        None
    """

    db: Session = next(get_db())

    try:
        api_providers = [
            ApiProvider(
                name="OpenAI",
                lowercase_name="openai",
                ai_models=[
                    "gpt-4",
                    "gpt-4-turbo",
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-3.5-turbo",
                ],
            ),
        ]

        db.add_all(api_providers)
        db.commit()

        print("API providers created successfully.")
    except IntegrityError:
        print(
            "An error occurred while creating API providers: duplicate entry."
        )
        db.rollback()
    except OperationalError:
        print(
            "An error occurred while creating API providers: database is not initialized."
        )
        db.rollback()
    except ProgrammingError:
        print(
            "An error occurred while creating API providers: tables are not created. Run 'alembic upgrade head' before running this script."
        )
        db.rollback()
    except SQLAlchemyError as e:
        print(f"An error occurred while creating API providers: {e}")
        db.rollback()


if __name__ == "__main__":
    create_api_providers()
