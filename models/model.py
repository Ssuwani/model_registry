from pydantic import BaseModel, Field
from enum import Enum


class Framework(Enum):
    pytorch = "pytorch"
    tensorflow = "tensorflow"
    sklearn = "sklearn"


class Model(BaseModel):
    name: str = Field(..., title="Name of the model")
    description: str = Field(..., title="Description of the model")
    version: str = Field(..., title="Version of the model")
    framework: Framework = Field(..., title="Framework of the model")
    metadata: dict = Field(..., title="Metadata of the model")
    model: object = Field(..., title="Model object")
