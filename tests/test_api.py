import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Support Ticket Decision Assistant API is running" in response.json()["message"]


def test_tickets_requires_authentication():
    response = client.get("/tickets")

    assert response.status_code in [401, 403]