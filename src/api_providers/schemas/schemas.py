from typing import Dict
from pydantic import BaseModel, RootModel, Field


class ApiProviderBase(BaseModel):
    """
    Schema for the base API provider.

    Attributes:
        value (str): The value of the provider.
        label (str): The label of the provider.
    """

    value: str
    label: str


class ApiProviderCollection(RootModel):
    """
    Schema for the collection of API providers.

    Attributes:
        root (Dict[str, ApiProviderBase]): A dictionary of providers.
    """

    root: Dict[str, ApiProviderBase]


class ApiProviderInfo(ApiProviderBase):
    """
    Schema for the response of API provider information with an additional field telling if the provider is disabled.

    Attributes:
        is_disabled (bool): Tells if the provider is disabled.
    """

    is_disabled: bool = Field(serialization_alias="isDisabled")


class ApiProviderResponse(RootModel):
    """
    Schema for the route response containing a collection of API providers with additional response-specific attributes.

    Attributes:
        root (Dict[str, ApiProviderInfo]): A dictionary of providers with additional attributes.
    """

    root: Dict[str, ApiProviderInfo]
