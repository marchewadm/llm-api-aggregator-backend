from fastapi import APIRouter

from src.dependencies import AuthDependency
from src.clients.external_dependencies import OpenAiApiKeyDependency


router = APIRouter(prefix="/openai", tags=["openai"])


@router.get("/models")
async def get_openai_models(
    auth: AuthDependency, api_key: OpenAiApiKeyDependency
):
    """
    Get the available OpenAI models.
    """

    print(api_key)

    return {"models": ["gpt-3", "gpt-4", "gpt-5"]}
