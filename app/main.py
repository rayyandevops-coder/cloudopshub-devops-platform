from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import os
import time
import logging

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("cloudopshub")

app = FastAPI(
    title="CloudOpsHub API",
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="Cloud-native DevOps/SRE portfolio API",
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

START_TIME = time.time()
ITEMS = [
    {"id": 1, "name": "kubernetes", "category": "orchestration"},
    {"id": 2, "name": "terraform", "category": "infrastructure"},
    {"id": 3, "name": "prometheus", "category": "observability"},
]


class Item(BaseModel):
    name: str
    category: str


@app.get("/")
def root():
    return {"service": "cloudopshub", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "cloudopshub"}


@app.get("/ready")
def ready():
    return {"status": "ready", "uptime_seconds": round(time.time() - START_TIME, 2)}


@app.get("/api/v1/info")
def info():
    return {
        "service": "CloudOpsHub API",
        "version": app.version,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "platform": "cloud-native",
    }


@app.get("/api/v1/items")
def list_items():
    return {"count": len(ITEMS), "items": ITEMS}


@app.post("/api/v1/items", status_code=201)
def create_item(item: Item):
    new_id = max([x["id"] for x in ITEMS], default=0) + 1
    record = {"id": new_id, **item.model_dump()}
    ITEMS.append(record)
    logger.info("created item id=%s", new_id)
    return record


@app.get("/api/v1/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
