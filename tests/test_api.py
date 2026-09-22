from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Cloud DevOps Infrastructure API is running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_storage():
    response = client.get("/storage")
    assert response.status_code == 200
    assert "bucket" in response.json()
    assert "objects" in response.json()