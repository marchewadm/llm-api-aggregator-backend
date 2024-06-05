import json
from fastapi import APIRouter

from .crud import crud

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from src.openapi.schemas.ai_models import (
    GetAiModelsResponse,
    GetUserAiModelNamesResponse,
)
from src.openapi.responses import get_user_ai_model_names_responses


router = APIRouter(prefix="/ai-models", tags=["ai-models"])


@router.get("/", response_model=GetAiModelsResponse)
async def get_ai_models():
    """
    Get a list of all AI models from JSON file.

    Returns:
    - GetAiModelsResponse: A list of all AI models.
    """

    with open("src/ai_models/models_data.json") as file:
        data = json.load(file)

    return data


@router.get(
    "/user",
    response_model=GetUserAiModelNamesResponse,
    responses={**get_user_ai_model_names_responses},
)
async def get_user_ai_model_names(auth: auth_dependency, db: db_dependency):
    """
    Retrieves all AI model names associated with the user based on the user's ID retrieved from the auth_dependency.

    Returns:
    - GetUserAiModelNamesResponse: A list of AI model names.
    - NotAuthenticatedException: If the user is not authenticated.
    """

    return crud.get_ai_models_by_user_id(db, auth["id"])
