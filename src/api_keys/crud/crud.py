from sqlalchemy.orm import Session, load_only

from src.api_keys.models import ApiKey
from src.api_keys.schemas.schemas import ApiKeySchema
from .crud_results import UpdateApiKeyResult


def get_api_keys_by_user_id(db: Session, user_id: int):
    """
    Retrieves all API keys from the database based on the user's ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        dict: A dictionary containing the AI model as the key and the API key as the value.
    """
    desired_fields = ["key", "ai_model"]
    fields = [getattr(ApiKey, field) for field in desired_fields]

    api_keys = (
        db.query(ApiKey)
        .options(load_only(*fields))
        .filter(ApiKey.user_id == user_id)  # noqa
        .all()
    )
    return {api_key.ai_model: api_key.key for api_key in api_keys}


def update_api_keys_by_user_id(
    db: Session, user_id: int, api_keys: list[ApiKeySchema]
) -> UpdateApiKeyResult:
    """
    Updates the API keys in the database based on the user's ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.
        api_keys (list[ApiKeySchema]): The new API keys.

    Returns:
        UpdateApiKeyResult: The result of the operation containing a message.
    """

    db_api_keys = get_api_keys_by_user_id(db, user_id)
    is_updated: bool = False

    for api_key in api_keys:
        if (
            api_key.ai_model in db_api_keys
            and api_key.key == db_api_keys[api_key.ai_model]
        ):
            continue
        elif (
            api_key.ai_model in db_api_keys
            and api_key.key != db_api_keys[api_key.ai_model]
        ):
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.ai_model == api_key.ai_model,  # noqa
                )
                .first()
            )
            db_api_key.key = api_key.key
            is_updated = True
        else:
            db_api_key = ApiKey(
                key=api_key.key, ai_model=api_key.ai_model, user_id=user_id
            )
            db.add(db_api_key)
            is_updated = True

    if is_updated:
        db.commit()
        return UpdateApiKeyResult(message="API keys updated successfully.")
    else:
        return UpdateApiKeyResult(
            message="Your API keys are already up to date. No changes were made."
        )
