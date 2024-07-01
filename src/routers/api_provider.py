from fastapi import APIRouter

from src.dependencies import ApiProviderServiceDependency
from src.schemas.api_provider import (
    ApiProviderCreate,
    ApiProviderCreateResponse,
    ApiProvidersResponse,
)


router = APIRouter(prefix="/api-provider", tags=["api-provider"])


# TODO: Create permissions dependency for this endpoint to allow only admin users to add new API providers
@router.post("", response_model=ApiProviderCreateResponse)
async def create_api_provider(
    payload: ApiProviderCreate,
    api_provider_service: ApiProviderServiceDependency,
):
    return api_provider_service.create_api_provider(payload)


@router.get("", response_model=ApiProvidersResponse)
async def get_api_providers(api_provider_service: ApiProviderServiceDependency):
    return api_provider_service.get_api_providers()
