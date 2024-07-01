from fastapi import Depends, HTTPException, status

from src.repositories.api_provider import ApiProviderRepository
from src.schemas.api_provider import (
    ApiProviderCreate,
    ApiProviderCreateResponse,
    ApiProvidersResponse,
)


class ApiProviderService:
    """
    Service for API provider related operations.
    """

    def __init__(
        self, repository: ApiProviderRepository = Depends(ApiProviderRepository)
    ) -> None:
        """
        Initializes the service with the repository.

        Args:
            repository (ApiProviderRepository): The repository to use for API provider operations.

        Returns:
            None
        """

        self.repository = repository

    def create_api_provider(
        self, payload: ApiProviderCreate
    ) -> ApiProviderCreateResponse:
        """
        Create a new API provider in the database.

        Args:
            payload (ApiProviderCreate): API provider creation payload containing name of the provider.

        Raises:
            HTTPException: Raised with status code 409 if the API provider already exists.

        Returns:
            ApiProviderCreateResponse: A message informing that the API provider was created.
            Message can be customized, but defaults to the one in the schema.
        """

        api_provider = self.repository.get_one(payload.lowercase_name)

        if api_provider:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="API provider already exists.",
            )
        self.repository.create(payload)

        return ApiProviderCreateResponse()

    def get_api_providers(self) -> ApiProvidersResponse:
        """
        Get all API providers.

        Returns:
            ApiProvidersResponse: A list of all available API providers.
        """

        return ApiProvidersResponse(api_providers=self.repository.get_many())
