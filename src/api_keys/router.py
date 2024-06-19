from fastapi import APIRouter

from .crud import crud

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency
from .dependencies import api_dependency

from .schemas.schemas import ApiKeySchema
from src.users.schemas.schemas import UserPassphrase

from src.openapi.schemas.api_keys import (
    GetApiKeysResponse,
    UpdateApiKeysResponse,
)
from src.openapi.responses import (
    get_api_keys_responses,
    update_api_keys_responses,
)


router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.get(
    "/", response_model=GetApiKeysResponse, responses={**get_api_keys_responses}
)
async def get_api_keys(auth: auth_dependency, db: db_dependency):
    """
    Retrieves all API keys from the database based on the user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with the user's API keys.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired).
    """

    result = crud.get_api_keys_by_user_id(db, auth["id"])
    return result


@router.post("/test")
async def get_test_keys(
    passphrase: UserPassphrase,
    auth: auth_dependency,
    db: db_dependency,
    fernet_key: api_dependency,
):
    """"""
    print(fernet_key)
    return


@router.patch(
    "/update",
    response_model=UpdateApiKeysResponse,
    responses={**update_api_keys_responses},
)
async def update_api_keys(
    auth: auth_dependency, db: db_dependency, user_data: list[ApiKeySchema]
):
    """
    Updates the API keys in the database based on the user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with a message if the operation is successful.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired).
    """

    result = crud.update_api_keys_by_user_id(db, auth["id"], user_data)
    return result
