import json

from sqlalchemy.orm import Session

from ..crud import crud
from ..schemas.schemas import DbAiModelCollection


def load_ai_models(db: Session, user_id: int):
    """"""

    user_ai_model_names = crud.get_user_ai_model_names(db, user_id)
    loaded_models = {}

    with open("src/ai_models/models_data.json") as file:
        data = DbAiModelCollection(**json.load(file))

    for k, v in data.root.items():
        is_disabled: bool = False

        if v.value in user_ai_model_names:
            is_disabled = True

        loaded_models.update(
            {k: {**v.model_dump(), "is_disabled": is_disabled}}
        )

    return loaded_models
