from fastapi import APIRouter

from .crud import crud

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from .schemas.schemas import ApiKeySchema


router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.get("/")
async def get_api_keys(auth: auth_dependency, db: db_dependency):
    """
    Retrieves all API keys from the database based on the user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with the user's API keys.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """
    result = crud.get_api_keys_by_user_id(db, auth["id"])
    return result


@router.patch("/update")
async def update_api_keys(
    auth: auth_dependency, db: db_dependency, user_data: list[ApiKeySchema]
):
    """
    Updates the API keys in the database based on the user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with a message if the operation is successful.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """
    result = crud.update_api_keys_by_user_id(db, auth["id"], user_data)
    return result
