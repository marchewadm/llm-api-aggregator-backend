from sqlalchemy.orm import Session, load_only

from src.api_keys.models import ApiKey
from .crud_results import UpdateApiKeyResult

from src.openapi.schemas.api_keys import GetApiKeysResponse
from src.api_keys.schemas.schemas import ApiKeySchema


def get_api_keys_by_user_id(db: Session, user_id: int) -> GetApiKeysResponse:
    """
    Retrieves all API keys from the database based on the user's ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        GetApiKeysResponse: A response object containing a list of API keys.
    """

    desired_fields = ["key", "ai_model"]
    fields = [getattr(ApiKey, field) for field in desired_fields]

    api_keys = (
        db.query(ApiKey)
        .options(load_only(*fields))
        .filter(ApiKey.user_id == user_id)  # noqa
        .all()
    )

    api_key_models = [
        ApiKeySchema(key=api_key.key, ai_model=api_key.ai_model)
        for api_key in api_keys
    ]

    return GetApiKeysResponse(api_key_models)


def get_ai_models_by_user_id(db: Session, user_id: int) -> list[str]:
    """
    Retrieves all AI models from the database based on the user's ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    # Returns:
    #     list[str]: A list of AI models.
    """

    ai_models = (
        db.query(ApiKey.ai_model)
        .filter(ApiKey.user_id == user_id)  # noqa
        .order_by(ApiKey.id.asc())
        .all()
    )

    return [ai_model[0] for ai_model in ai_models]


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

    db_api_keys = get_api_keys_by_user_id(db, user_id).model_dump()
    user_api_keys = {api_key.ai_model: api_key.key for api_key in api_keys}
    is_updated: bool = False

    for ai_model, api_key in user_api_keys.items():
        different_key_exists = any(
            item["ai_model"] == ai_model and item["key"] != api_key
            for item in db_api_keys
        )
        same_key_exists = any(
            item["ai_model"] == ai_model and item["key"] == api_key
            for item in db_api_keys
        )

        if different_key_exists:
            # If ai_model is present in the database but the key is different, update the key.
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.ai_model == ai_model,  # noqa
                )
                .first()
            )

            db_api_key.key = api_key
            is_updated = True
        elif not same_key_exists:
            # If ai_model is not present in the database, add new record to the database.
            new_api_key = ApiKey(
                key=api_key, ai_model=ai_model, user_id=user_id
            )
            db.add(new_api_key)
            is_updated = True

    for record in db_api_keys:
        if record["ai_model"] not in user_api_keys:
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.ai_model == record["ai_model"],
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
