from fastapi import APIRouter

from src.dependencies import AuthDependency, ApiKeyServiceDependency


router = APIRouter(prefix="/api-key", tags=["api-key"])


@router.get("")
async def get_api_keys(
    auth: AuthDependency,
    api_key_service: ApiKeyServiceDependency,
):
    return api_key_service.get_user_api_keys(auth.user_id)
