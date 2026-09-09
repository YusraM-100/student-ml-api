import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "wrong"
    assert data["application"] == "student-ml-api"
    assert "version" in data


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input(client):
    response = client.post("/predict", json={})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_predict_invalid_input(client):
    response = client.post("/predict", json={"value": "not-a-number"})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
