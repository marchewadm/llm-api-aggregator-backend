from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .crud import crud
from .schemas.schemas import UserUpdatePassword, UserUpdateProfile
from .schemas.response_schemas import (
    GetUserProfileResponse,
    UpdateUserPasswordResponse,
    UpdateUserProfileResponse,
)
from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from src.exceptions import UserNotFoundException, BadRequestException
from .openapi_responses import (
    get_profile_responses,
    update_password_responses,
    update_profile_responses,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/profile",
    response_model=GetUserProfileResponse,
    responses={**get_profile_responses},
)
async def get_profile(auth: auth_dependency, db: db_dependency):
    """
    Retrieves the user's profile information from the database by user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with the user's profile information.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """

    result = crud.get_desired_fields_by_user_id(
        db, auth["id"], ["name", "email", "avatar"]
    )
    return result


@router.patch(
    "/update-password",
    response_model=UpdateUserPasswordResponse,
    responses={**update_password_responses},
)
async def update_password(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdatePassword
):
    """
    Updates the user's password in the database by user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with a message if the operation is successful.
    - A UserNotFoundException if the user is not found in the database.
    - A BadRequestException if the user's password is incorrect.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """

    result = crud.update_user_password(db, auth["id"], user_data)
    if not result.is_success:
        if result.status_code == 404:
            raise UserNotFoundException(message=result.message)
        if result.status_code == 400:
            raise BadRequestException(message=result.message)
    return result.message


@router.patch(
    "/update-profile",
    response_model=UpdateUserProfileResponse,
    responses={**update_profile_responses},
)
async def update_profile(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdateProfile
):
    """
    Updates the user's profile in the database by user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with updated data if the operation is successful.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """

    result = crud.update_user_profile(db, auth["id"], user_data)
    return result
