from sqlalchemy.orm import Session, load_only

from src.database.models import ApiKey
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

    desired_fields = ["key", "api_provider"]
    fields = [getattr(ApiKey, field) for field in desired_fields]

    api_keys = (
        db.query(ApiKey)
        .options(load_only(*fields))
        .filter(ApiKey.user_id == user_id)  # noqa
        .all()
    )

    api_key_models = [
        ApiKeySchema(key=api_key.key, api_provider=api_key.api_provider)
        for api_key in api_keys
    ]

    return GetApiKeysResponse(api_key_models)


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
    user_api_keys = {api_key.api_provider: api_key.key for api_key in api_keys}
    is_updated: bool = False

    for api_provider, api_key in user_api_keys.items():
        different_key_exists = any(
            item["api_provider"] == api_provider and item["key"] != api_key
            for item in db_api_keys
        )
        same_key_exists = any(
            item["api_provider"] == api_provider and item["key"] == api_key
            for item in db_api_keys
        )

        if different_key_exists:
            # If api_provider is present in the database but the key is different, update the key.
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.api_provider == api_provider,  # noqa
                )
                .first()
            )

            db_api_key.key = api_key
            is_updated = True
        elif not same_key_exists:
            # If api_provider is not present in the database, add new record to the database.
            new_api_key = ApiKey(
                key=api_key, api_provider=api_provider, user_id=user_id
            )
            db.add(new_api_key)
            is_updated = True

    for record in db_api_keys:
        if record["api_provider"] not in user_api_keys:
            db_api_key = (
                db.query(ApiKey)
                .filter(
                    ApiKey.user_id == user_id,  # noqa
                    ApiKey.api_provider == record["api_provider"],
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
