from minio import Minio
from config import MinIOSettings

minio_settings = MinIOSettings()


class MinioDatasource:
    def __init__(
        self,
        endpoint=minio_settings.ENDPOINT,
        access_key=minio_settings.ACCESS_KEY,
        secret_key=minio_settings.SECRET_KEY,
    ):
        self.client = Minio(endpoint, access_key, secret_key, secure=False)

    def list_objects(self, bucket_name):
        return self.client.list_objects(bucket_name)

    def __enter__(self):
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
