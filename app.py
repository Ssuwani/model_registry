from fastapi import FastAPI
from datasources.db import DB
from routers.model import router
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    with DB("model_registry.db") as db:
        db.query(
            "CREATE TABLE IF NOT EXISTS models (name TEXT, description TEXT, version TEXT, framework TEXT, metadata TEXT, storage_path TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (name, version))"
        )
    logger.info("DB ready")
