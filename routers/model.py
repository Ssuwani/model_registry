from fastapi.routing import APIRouter
from handlers.model import (
    get_model,
    list_models,
    delete_model,
)

router = APIRouter()


@router.get("/models")
def list_models_router():
    return list_models()


@router.get("/models/{model_name}/{version}")
def get_model_router(model_name: str, version: str):
    model = get_model(model_name, version, raw_data=True)
    return model


@router.delete("/models/{model_name}")
def delete_model_router(model_name: str) -> str:
    delete_model(model_name)
    return "ok"
