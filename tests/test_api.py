from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_info():
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.json()["service"] == "CloudOpsHub API"


def test_items():
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json()["count"] >= 3
