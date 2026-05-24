from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}


def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 200
    assert "error" in response.json()


def test_health():
    """Test the health endpoint returns 200 with status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
