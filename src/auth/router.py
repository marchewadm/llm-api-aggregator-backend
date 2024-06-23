from fastapi import APIRouter

from src.dependencies import UserServiceDependency

from .schemas import UserRegister, UserRegisterResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(
    payload: UserRegister, user_service: UserServiceDependency
):
    result = user_service.create(payload)
    return result
