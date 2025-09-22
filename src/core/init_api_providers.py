import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.core.database import get_db
from src.api_provider.models import ApiProvider
from src.logger.logger import init_logging


init_logging()
logger = logging.getLogger(__name__)


OpenAiProvider = ApiProvider(
    name="OpenAI",
    lowercase_name="openai",
    ai_models=[
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
    ],
)

GeminiProvider = ApiProvider(
    name="Gemini",
    lowercase_name="gemini",
    ai_models=[
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
        "gemini-1.0-pro",
    ],
)


def create_api_providers() -> None:
    """
    Initializes the database with predefined API providers.

    This function inserts a set of predefined API providers into the database. Each provider is associated
    with a list of AI models it supports. It is intended to be run only once during the application's
    first-time setup to ensure that the necessary data exists in the database.

    IMPORTANT: Before running this function, ensure that:
    1. The database is initialized.
    2. The necessary tables are created by executing the migration command:
       `alembic upgrade head`.

    Returns:
        None
    """

    db: Session = next(get_db())
    api_providers = [OpenAiProvider, GeminiProvider]

    try:
        new_providers = [
            provider
            for provider in api_providers
            if not db.scalar(
                select(ApiProvider).where(
                    ApiProvider.lowercase_name == provider.lowercase_name
                )
            )
        ]

        if new_providers:
            db.add_all(new_providers)
            db.commit()
            logger.info("API providers created successfully.")
        else:
            logger.info("API providers already exist in the database.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"An error occurred while creating API providers: {e}")


if __name__ == "__main__":
    create_api_providers()
