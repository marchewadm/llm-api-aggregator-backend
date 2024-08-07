from fastapi import APIRouter

from .dependencies import ApiProviderServiceDependency
from .schemas import (
    ApiProviderCreateRequest,
    ApiProviderCreateResponse,
    ApiProviderResponse,
    ApiProvidersResponse,
)


router = APIRouter(prefix="/api-provider", tags=["api-provider"])


# TODO: Create permissions dependency for this endpoint to allow only admin users to add new API providers
@router.post("", response_model=ApiProviderCreateResponse)
async def create_api_provider(
    payload: ApiProviderCreateRequest,
    api_provider_service: ApiProviderServiceDependency,
):
    """
    Create a new API provider and return message containing the status of the operation.
    """

    return api_provider_service.create(payload)


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


# TODO: Create permissions dependency for this endpoint to allow only admin users to delete API providers
@router.delete("/{api_provider_id}")
async def delete_api_provider(
    api_provider_id: int, api_provider_service: ApiProviderServiceDependency
):
    """
    Delete an API provider by its ID.
    """

    return api_provider_service.delete_by_id(api_provider_id)
