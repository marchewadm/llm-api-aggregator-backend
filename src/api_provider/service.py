from fastapi import Depends, HTTPException, status

from src.shared.service.base import BaseService

from .repository import ApiProviderRepository
from .schemas import (
    ApiProviderCreateRequest,
    ApiProviderCreateResponse,
    ApiProvidersResponse,
)


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

    def create(
        self, payload: ApiProviderCreateRequest
    ) -> ApiProviderCreateResponse:
        """
        Create new API provider and store it in the database.

        Args:
            payload (ApiProviderCreateRequest): Pydantic model containing the data to create the entity with.

        Raises:
            HTTPException: Raised with status code 409 if the API provider already exists.

        Returns:
            ApiProviderCreateResponse: A message informing that the API provider was created.
                Message can be customized, but defaults to the one in the schema.
        """

        api_provider = (
            self.repository.get_one_with_selected_attributes_by_condition(
                ["id"],
                "lowercase_name",
                payload.lowercase_name,
            )
        )

        if api_provider:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"API provider {payload.name} already exists. Name must be unique.",
            )
        self.repository.create(payload.model_dump())

        return ApiProviderCreateResponse()

    def get_all(self) -> ApiProvidersResponse:
        """
        Get all API providers.

        TODO: self.repository.get_all() returns a sequence of APIProvider objects,
            but the response model expects a list of ApiProvider objects.

        Returns:
            ApiProvidersResponse: A list of all available API providers.
        """

        api_providers = self.repository.get_all()

        return ApiProvidersResponse(api_providers=api_providers)
