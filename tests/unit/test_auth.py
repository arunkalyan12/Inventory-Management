# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from components.inventory_management.api.auth import router as auth_router
from fastapi import FastAPI
from components.inventory_management.db import mongo_queries as mq

# Create FastAPI app for testing
app = FastAPI()
app.include_router(auth_router)

client = TestClient(app)


# ---- Setup test database ----
@pytest.fixture(autouse=True)
def setup_test_db():
    test_client = MongoClient("mongodb://localhost:27017")
    test_db = test_client["test_inventory_db_auth"]
    mq.USERS_COLLECTION = test_db["users"]
    mq.USERS_COLLECTION.delete_many({})
    yield
    mq.USERS_COLLECTION.delete_many({})


# ---- Tests ----


def test_signup_success():
    response = client.post(
        "/signup",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "strongpassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "Signup successful"


def test_signup_duplicate_email():
    client.post(
        "/signup",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "strongpassword",
        },
    )
    response = client.post(
        "/signup",
        json={
            "full_name": "Another User",
            "email": "testuser@example.com",
            "password": "anotherpassword",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    client.post(
        "/signup",
        json={
            "full_name": "Login User",
            "email": "loginuser@example.com",
            "password": "loginpass",
        },
    )
    response = client.post(
        "/login", json={"email": "loginuser@example.com", "password": "loginpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "Login successful"


def test_login_wrong_password():
    client.post(
        "/signup",
        json={
            "full_name": "Wrong Pass User",
            "email": "wrongpass@example.com",
            "password": "rightpass",
        },
    )
    response = client.post(
        "/login", json={"email": "wrongpass@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_nonexistent_user():
    response = client.post(
        "/login", json={"email": "nonexistent@example.com", "password": "nopassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_signup_full_name():
    """Test that the user is created with the correct full name."""
    response = client.post(
        "/signup",
        json={
            "full_name": "Full Name User",
            "email": "fullnameuser@example.com",
            "password": "securepass",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "Signup successful"

    user_id = data["user_id"]
    user = mq.USERS_COLLECTION.find_one({"_id": mq.ObjectId(user_id)})
    assert user is not None
    assert (
        user["full_name"] == "Full Name User"
    ), f"Expected full_name to be 'Full Name User', got {user['full_name']}"
