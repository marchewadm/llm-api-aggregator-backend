from fastapi import APIRouter

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from .services.service import get_api_providers
from .schemas.schemas import ApiProviderResponse

from src.openapi.responses import get_api_providers_responses


router = APIRouter(prefix="/api-providers", tags=["api-providers"])


@router.get(
    "/",
    response_model=ApiProviderResponse,
    responses={**get_api_providers_responses},
)
async def get_api_providers(auth: auth_dependency, db: db_dependency):
    result = get_api_providers(db, auth["id"])
    return result
