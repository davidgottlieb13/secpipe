"""
Basic test suite for the SecPipe API.
Run with: pytest

This is intentionally simple, but it's real enough to matter: it's what the
CI pipeline will run in Phase 1's first pipeline stage, and it's what a
vulnerable-dependency-triggered pipeline failure will still need to pass
alongside the security gates added in Phase 3.
"""

from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item():
    create_response = client.post("/items", json={"name": "Test Item", "description": "A test"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Item"


def test_list_items():
    client.post("/items", json={"name": "Another Item"})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_nonexistent_item_returns_404():
    response = client.get("/items/99999")
    assert response.status_code == 404


def test_delete_item():
    create_response = client.post("/items", json={"name": "To Delete"})
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
