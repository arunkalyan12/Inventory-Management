# tests/test_inventory_user.py

import pytest
from pymongo import MongoClient
from components.inventory_management.db import mongo_queries as mq
from components.inventory_management.db.models import User, InventoryItem


# -------------------- Setup Test DB --------------------
@pytest.fixture(autouse=True)
def setup_test_db():
    test_client = MongoClient("mongodb://localhost:27017")
    test_db = test_client["test_inventory_test_db"]

    # Override collections
    mq.USERS_COLLECTION = test_db["users"]
    mq.ITEMS_COLLECTION = test_db["items"]

    # Clear collections before test
    mq.USERS_COLLECTION.delete_many({})
    mq.ITEMS_COLLECTION.delete_many({})

    yield

    # Clear collections after test
    mq.USERS_COLLECTION.delete_many({})
    mq.ITEMS_COLLECTION.delete_many({})


# -------------------- User Tests --------------------
def test_insert_and_get_user():
    user = User(full_name="Test User", email="test@example.com", password_hash="hashed")
    user_id = mq.insert_user(user)

    fetched_user = mq.get_user_by_id(user_id)
    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"
    assert fetched_user.full_name == "Test User"


# -------------------- Inventory Tests --------------------
def test_insert_inventory_for_user():
    user = User(
        full_name="Inventory User", email="inv@example.com", password_hash="hashed"
    )
    user_id = mq.insert_user(user)

    mq.insert_inventory_for_user(user_id)

    items = list(mq.ITEMS_COLLECTION.find({"user_id": user_id}))
    assert len(items) == 2
    assert all(item["user_id"] == user_id for item in items)


def test_update_inventory_item_quantity():
    user = User(
        full_name="Quantity User", email="qty@example.com", password_hash="hashed"
    )
    user_id = mq.insert_user(user)

    item = InventoryItem(
        user_id=user_id,
        name="Apple",
        category_id="cat1",
        location_id="loc1",
        quantity=5,
    )
    item_id = mq.insert_item(item)

    updated_item = mq.update_quantity(item_id, 3)
    assert updated_item.quantity == 8

    updated_item = mq.update_quantity(item_id, -2)
    assert updated_item.quantity == 6


def test_list_items_for_specific_user():
    user1 = User(full_name="User 1", email="user1@example.com", password_hash="hashed")
    user2 = User(full_name="User 2", email="user2@example.com", password_hash="hashed")
    user1_id = mq.insert_user(user1)
    user2_id = mq.insert_user(user2)

    mq.insert_item(
        InventoryItem(
            user_id=user1_id, name="Item A", category_id="cat1", location_id="loc1"
        )
    )
    mq.insert_item(
        InventoryItem(
            user_id=user2_id, name="Item B", category_id="cat1", location_id="loc1"
        )
    )

    items_user1 = mq.list_items({"user_id": user1_id})
    assert len(items_user1) == 1
    assert items_user1[0].user_id == user1_id
    assert items_user1[0].name == "Item A"


def test_update_item_user_specific():
    user1 = User(full_name="User 1", email="user1@example.com", password_hash="hashed")
    user2 = User(full_name="User 2", email="user2@example.com", password_hash="hashed")
    user1_id = mq.insert_user(user1)
    user2_id = mq.insert_user(user2)

    item1_id = mq.insert_item(
        InventoryItem(
            user_id=user1_id, name="Item 1", category_id="cat1", location_id="loc1"
        )
    )
    item2_id = mq.insert_item(
        InventoryItem(
            user_id=user2_id, name="Item 2", category_id="cat1", location_id="loc1"
        )
    )

    updated_item = mq.update_item(item1_id, {"quantity": 99})
    assert updated_item.quantity == 99
    assert updated_item.user_id == user1_id

    other_item = mq.get_item_by_id(item2_id)
    assert other_item.quantity == 0
