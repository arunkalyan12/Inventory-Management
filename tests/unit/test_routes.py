# tests/unit/test_routes.py
from backend.app import app  # Correct import
from fastapi.testclient import TestClient
import sys
import os

# Add the backend folder to sys.path so Python can find the app module
sys.path.append(os.path.join(os.path.dirname(__file__), "../../backend"))

client = TestClient(app)


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Inventory Management API is running!"}


def test_inventory_route():
    # Include trailing slash to match FastAPI router
    response = client.get("/inventory/")
    assert response.status_code == 200
    # Replace with your actual inventory_router response if needed
    assert isinstance(response.json(), dict)


def test_shopping_list_route():
    response = client.get("/shopping-list/")  # Include trailing slash
    assert response.status_code == 200
    data = response.json()
    # Check for shopping list key
    assert "shopping_list" in data


def test_auth_signup():
    payload = {
        "email": "test@example.com",
        "password": "securepassword",
        "full_name": "Test User",
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "email" in data or "message" in data


def test_auth_login():
    signup_payload = {
        "email": "test@example.com",
        "password": "securepassword",
        "full_name": "Test User",
    }
    client.post("/auth/signup", json=signup_payload)

    login_payload = {"email": "test@example.com", "password": "securepassword"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data or "message" in data


if __name__ == "__main__":
    test_root_route()
    test_inventory_route()
    test_shopping_list_route()
    test_auth_signup()
    test_auth_login()
    print("All tests passed!")
