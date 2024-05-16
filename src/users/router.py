from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .crud import crud
from .schemas.schemas import UserUpdatePassword, UserUpdateProfile
from .schemas.response_schemas import (
    GetUserProfileResponse,
    UpdateUserPasswordResponse,
)
from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from src.exceptions import UserNotFoundException, ConflictException
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
    return crud.get_desired_fields_by_user_id(
        db, auth["id"], ["name", "email", "avatar"]
    )


@router.patch(
    "/update-password",
    response_model=UpdateUserPasswordResponse,
    responses={**update_password_responses},
)
async def update_password(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdatePassword
):
    result = crud.update_user_password(db, auth["id"], user_data)
    if not result.is_success:
        if result.status_code == 404:
            raise UserNotFoundException(message=result.message)
        if result.status_code == 409:
            raise ConflictException(message=result.message)
    return JSONResponse(content={"message": result.message})


@router.patch("/update-profile", responses={**update_profile_responses})
async def update_profile(
    auth: auth_dependency, db: db_dependency, user_data: UserUpdateProfile
):
    return crud.update_user_profile(db, auth["id"], user_data)
