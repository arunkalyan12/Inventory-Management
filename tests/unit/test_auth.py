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
    # Connect to MongoDB test database
    test_client = MongoClient("mongodb://localhost:27017")
    test_db = test_client["test_inventory_db_auth"]

    # Override USERS_COLLECTION to use test database
    mq.USERS_COLLECTION = test_db["users"]
    mq.USERS_COLLECTION.delete_many({})  # Clean before test

    yield

    # Clean up after test
    mq.USERS_COLLECTION.delete_many({})


# ---- Tests ----
def test_signup_success():
    response = client.post(
        "/signup", json={"email": "testuser@example.com", "password": "strongpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "User created successfully"


def test_signup_duplicate_email():
    # First signup
    client.post(
        "/signup", json={"email": "testuser@example.com", "password": "strongpassword"}
    )
    # Second signup with same email
    response = client.post(
        "/signup", json={"email": "testuser@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    # Signup first
    client.post(
        "/signup", json={"email": "loginuser@example.com", "password": "loginpass"}
    )
    # Login
    response = client.post(
        "/login", json={"email": "loginuser@example.com", "password": "loginpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["message"] == "Login successful"


def test_login_wrong_password():
    # Signup first
    client.post(
        "/signup", json={"email": "wrongpass@example.com", "password": "rightpass"}
    )
    # Attempt login with wrong password
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
