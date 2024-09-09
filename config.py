from pydantic_settings import BaseSettings
from pydantic import Field


class MinIOSettings(BaseSettings):
    ENDPOINT: str = Field("localhost:9000")
    ACCESS_KEY: str = Field("minio")
    SECRET_KEY: str = Field("minioadmin")

    class Config:
        env_prefix = "MINIO_"  # 환경 변수 접두사
