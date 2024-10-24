from fastapi import APIRouter

from .dependencies import ApiProviderServiceDependency
from .schemas import (
    ApiProviderResponse,
    ApiProvidersResponse,
)


router = APIRouter(prefix="/api-provider", tags=["api-provider"])


@router.get("/all", response_model=ApiProvidersResponse)
async def get_api_providers_names(
    api_provider_service: ApiProviderServiceDependency,
):
    """
    Get all API providers names and their IDs.
    """

    return api_provider_service.get_all()


@router.get("/{api_provider_id}", response_model=ApiProviderResponse)
async def get_api_provider_by_id(
    api_provider_id: int, api_provider_service: ApiProviderServiceDependency
):
    """
    Get full information about an API provider by its ID.
    """

    return api_provider_service.get_one_by_id(api_provider_id)
