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
    new_api_keys_map = {api_key.ai_model: api_key.key for api_key in api_keys}
    is_updated: bool = False

    # Update existing keys and add new keys
    for ai_model, new_key in new_api_keys_map.items():
        if ai_model in db_api_keys:
            if db_api_keys[ai_model] != new_key:
                # Update the key in the database
                db_api_key = (
                    db.query(ApiKey)
                    .filter(
                        ApiKey.user_id == user_id,  # noqa
                        ApiKey.ai_model == ai_model,  # noqa
                    )
                    .first()
                )
                db_api_key.key = new_key
                is_updated = True
        else:
            # Add new key to the database
            new_api_key = ApiKey(
                key=new_key, ai_model=ai_model, user_id=user_id
            )
            db.add(new_api_key)
            is_updated = True

    # Remove keys that are no longer present in the new list
    for ai_model in db_api_keys:
        if ai_model not in new_api_keys_map:
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.ai_model == ai_model,  # noqa
                )
                .first()
            )
            db.delete(db_api_key)
            is_updated = True

    if is_updated:
        db.commit()
        return UpdateApiKeyResult(message="API keys updated successfully.")
    else:
        return UpdateApiKeyResult(
            message="Your API keys are already up to date. No changes were made."
        )
