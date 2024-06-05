import json
from fastapi import APIRouter

from .crud import crud

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency

from src.openapi.schemas.ai_models import GetAiModelsResponse


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


@router.get("/user")
async def get_user_ai_models(auth: auth_dependency, db: db_dependency):
    """
    Retrieves all AI models associated with the user based on the user's ID retrieved from the auth_dependency.

    Returns:
    - A JSONResponse with the user's AI models.
    - A NotAuthenticatedException if the user is not authenticated (e.g. token is invalid or expired)
    """

    return crud.get_ai_models_by_user_id(db, auth["id"])
