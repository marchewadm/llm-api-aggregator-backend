from fastapi import Depends, HTTPException, status

from src.repositories.api_provider import ApiProviderRepository
from src.schemas.api_provider import (
    ApiProviderCreate,
    ApiProviderCreateResponse,
    ApiProvidersResponse,
)

from .base import BaseService


class ApiProviderService(BaseService[ApiProviderRepository]):
    """
    Service for API provider related operations.
    """

    def __init__(
        self, repository: ApiProviderRepository = Depends(ApiProviderRepository)
    ):
        """
        Initialize the service with the repository.

        Args:
            repository (ApiProviderRepository): The repository to use for API provider operations.

        Returns:
            None
        """

        super().__init__(repository)

    def create(self, payload: ApiProviderCreate) -> ApiProviderCreateResponse:
        """
        Create new API provider and store it in the database.

        Args:
            payload (ApiProviderCreate): Pydantic model containing the data to create the entity with.

        Raises:
            HTTPException: Raised with status code 409 if the API provider already exists.

        Returns:
            ApiProviderCreateResponse: A message informing that the API provider was created.
                Message can be customized, but defaults to the one in the schema.
        """

        api_provider = self.repository.get_one_by_name(payload.lowercase_name)

        if api_provider:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="API provider already exists.",
            )
        self.repository.create(payload.model_dump())

        return ApiProviderCreateResponse()

    def get_all(self) -> ApiProvidersResponse:
        """
        Get all API providers.

        Returns:
            ApiProvidersResponse: A list of all available API providers.
        """

        return ApiProvidersResponse(api_providers=self.repository.get_all())
