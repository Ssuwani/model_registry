from models.model import Model, Framework
from datasources.db import DB
from datasources.minio import MinioDatasource
import json
from zoneinfo import ZoneInfo
from datetime import datetime
import os
import joblib
import torch
import tensorflow as tf


def create_model(model: Model):
    """
    Create a model in the registry
    :param model:
    :return:
    """
    with DB("model_registry.db") as db:
        metadata = json.dumps(model.metadata)  # 직렬화해서 저장
        storage_path = save_model_on_minio(model)
        db.query(
            f"INSERT INTO models (name, description, version, framework, metadata, storage_path) VALUES ('{model.name}', '{model.description}', '{model.version}', '{model.framework.value}', '{metadata}', '{storage_path}')"
        )
    return "ok"


def update_model(model: Model):
    """
    Update a model in the registry
    :param model:
    :return:
    """
    with DB("model_registry.db") as db:
        metadata = json.dumps(model.metadata)
        storage_path = save_model_on_minio(model)
        db.query(
            f"UPDATE models SET description = '{model.description}', framework = '{model.framework.value}', metadata = '{metadata}', storage_path = '{storage_path}' WHERE name = '{model.name}' AND version = '{model.version}'"
        )
    return "ok"


def delete_model(model_name: str) -> str:
    """
    Delete a model from the registry
    :param model_name
    """
    with DB("model_registry.db") as db:
        db.query(f"DELETE FROM models WHERE name = '{model_name}'")
    return "ok"


def list_models():
    """
    List all models in the registry
    :return: list of Model
    """
    with DB("model_registry.db") as db:
        models = db.query("SELECT name, version FROM models").fetchall()
    return models


def get_model(
    model_name: str, version: str = "latest", raw_data: bool = False
) -> Model | None:
    """
    Get a model from the registry
    :param model_name:
    :param version:
    :return: Model
    """
    with DB("model_registry.db") as db:
        if version == "latest":
            model = db.query(
                f"SELECT name, description, version, framework, metadata, storage_path FROM models WHERE name = '{model_name}' ORDER BY version DESC LIMIT 1"
            ).fetchone()
        else:
            model = db.query(
                f"SELECT name, description, version, framework, metadata, storage_path FROM models WHERE name = '{model_name}' AND version = '{version}'"
            ).fetchone()
    if raw_data:
        return model
    return Model(
        name=model[0],
        description=model[1],
        version=model[2],
        framework=model[3],
        metadata=json.loads(model[4]),
        model=load_model_from_minio(
            storage_path=model[5],
            framework=model[3],
        ),
    )


def load_model_from_minio(storage_path: str, framework: Framework) -> object:
    """
    Load a model from Minio
    :param storage_path:
    :return: Model
    """
    with MinioDatasource() as minio:
        minio.fget_object("models", storage_path, storage_path)

    if framework == Framework.sklearn.value:
        model = joblib.load(storage_path)
    elif framework == Framework.tensorflow.value:
        model = tf.keras.models.load_model(storage_path)
    elif framework == Framework.pytorch.value:
        model = torch.load(storage_path)
    return model


def save_model_on_minio(model: Model) -> str:
    """
    Save a model on Minio
    :param model:
    :return: storage path
    """
    now = datetime.now(tz=ZoneInfo("Asia/Seoul")).strftime("%Y%m%d%H%M%S")
    storage_path = f"models/{model.name}/{now}/"
    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    if model.framework == Framework.sklearn:
        storage_path += "model.joblib"
        joblib.dump(model.model, storage_path)
    elif model.framework == Framework.tensorflow:
        storage_path += "model.keras"
        model.model.save(storage_path)
    elif model.framework == Framework.pytorch:
        storage_path += "model.pth"
        torch.save(model.model, storage_path)

    with MinioDatasource() as minio:
        minio.fput_object("models", storage_path, storage_path)
    return storage_path
