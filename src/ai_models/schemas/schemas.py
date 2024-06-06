from pydantic import RootModel, BaseModel, Field
from typing import Dict


class AiModelInfo(BaseModel):
    """
    Schema for model information.

    Attributes:
        value (str): The value of the model.
        label (str): The label of the model.
    """

    value: str
    label: str


class DbAiModelCollection(RootModel):
    """
    Schema for the CRUD response containing a collection of models from the database.

    Attributes:
        root (Dict[str, ModelInfo]): A dictionary of models.
    """

    root: Dict[str, AiModelInfo]


class AiModelInfoResponse(AiModelInfo):
    """
    Schema for the response of model information with an additional field to indicate if the model is disabled.

    Attributes:
        is_disabled (bool): Indicates if the model is disabled.
    """

    is_disabled: bool = Field(serialization_alias="isDisabled")


class AiModelResponseCollection(RootModel):
    """
    Schema for the response containing a collection of models with additional response-specific attributes.

    Attributes:
        root (Dict[str, ModelInfoResponse]): A dictionary of model responses.
    """

    root: Dict[str, AiModelInfoResponse]
