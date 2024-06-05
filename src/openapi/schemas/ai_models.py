from pydantic import RootModel, BaseModel
from typing import Dict, List


class AiModel(BaseModel):
    """
    Schema for an AI model.

    Attributes:
        - value (str): The value of the AI model.
        - label (str): The label of the AI model.
    """

    value: str
    label: str


class GetAiModelsResponse(RootModel):
    """
    Schema for the response body of the GET /ai-models endpoint.

    Attributes:
        - root (Dict[str, AiModel]): A dictionary of AI models.
    """

    root: Dict[str, AiModel]


class GetUserAiModelNamesResponse(RootModel):
    root: List[str]
