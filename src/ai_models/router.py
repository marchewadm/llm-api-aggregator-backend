import json
from fastapi import APIRouter

from src.openapi.schemas.ai_models import GetAiModelsResponse


router = APIRouter(prefix="/ai-models", tags=["ai-models"])


@router.get("/", response_model=GetAiModelsResponse)
async def get_ai_models():
    """
    Get a list of all AI models.

    Returns:
        - GetAiModelsResponse: A list of all AI models.
    """

    with open("src/ai_models/models_data.json") as file:
        data = json.load(file)

    return data
