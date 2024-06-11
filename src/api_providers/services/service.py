import json

from sqlalchemy.orm import Session

from ..crud import crud
from ..schemas.schemas import ApiProviderCollection


def get_api_providers(db: Session, user_id: int):
    """
    This function retrieves all API providers associated with a specific user from the database. It then compares
    these user-specific API providers with all available API providers listed in the 'models_data.json' file.

    The function returns a dictionary of API providers. Each entry in the dictionary includes all the information
    about the API provider from the 'models_data.json' file, along with an additional field 'is_disabled'. This
    field indicates whether the user is already using the API provider.

    Args:
        db (Session): The database session object used to interact with the database.
        user_id (int): The ID of the user for whom the API providers are being retrieved.

    Returns:
        dict: A dictionary where each key is the name of an API provider and the value is a dictionary containing
        information about the API provider and the 'is_disabled' field.

    TODO: consider adding type hints for the return value.

    TODO: consider creating another table in the database to store all the available API providers and their details.

    TODO: consider renaming "is_disabled" to maybe "is_used" or something similar for clarity.
    TODO: "is_disabled" might be confusing. It could be interpreted as the API provider being disabled, not used.
    """

    user_api_providers = crud.get_user_api_providers(db, user_id)
    api_providers = {}

    with open("src/api_providers/api_providers.json") as file:
        api_providers_collection = ApiProviderCollection(**json.load(file))

    for k, v in api_providers_collection.root.items():
        is_disabled: bool = False

        if v.value in user_api_providers:
            is_disabled = True

        api_providers.update(
            {k: {**v.model_dump(), "is_disabled": is_disabled}}
        )

    return api_providers
