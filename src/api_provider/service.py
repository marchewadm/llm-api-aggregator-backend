from fastapi import Depends

from src.shared.service.base import BaseService

from .repository import ApiProviderRepository
from .schemas import (
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
