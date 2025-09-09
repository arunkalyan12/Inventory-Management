from app import app
from fastapi.testclient import TestClient
import sys
import os

# Add the backend folder to sys.path so Python can find the app module
sys.path.append(os.path.join(os.path.dirname(__file__), "../../backend"))

# import pytest

client = TestClient(app)


def test_inventory_route():
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == {"message": "Inventory Management API is running!"}


def test_shopping_list_route():
    response = client.get("/shopping-list")
    assert response.status_code == 200
    assert response.json() == {"message": "Shopping List API is running!"}


def test_auth_signup():
    payload = {"email": "test@example.com", "password": "securepassword"}
    response = client.post("/auth/signup", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "message" in data or "email" in data


def test_auth_login():
    signup_payload = {"email": "test@example.com", "password": "securepassword"}
    client.post("/auth/signup", json=signup_payload)

    login_payload = {"email": "test@example.com", "password": "securepassword"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data or "message" in data
