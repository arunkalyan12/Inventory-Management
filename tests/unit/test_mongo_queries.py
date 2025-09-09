# tests/test_inventory_category_location.py

import pytest
from pymongo import MongoClient
from components.inventory_management.db import mongo_queries as mq
from components.inventory_management.db.models import InventoryItem, Category, Location


# -------------------- Setup Test DB --------------------
@pytest.fixture(scope="module", autouse=True)
def test_db():
    """
    Connect to a test database and override collections.
    """
    client = MongoClient("mongodb://localhost:27017")
    db = client["test_inventory_db"]

    mq.ITEMS_COLLECTION = db["items"]
    mq.CATEGORIES_COLLECTION = db["categories"]
    mq.LOCATIONS_COLLECTION = db["locations"]

    # Clean collections before tests
    for coll in [
        mq.ITEMS_COLLECTION,
        mq.CATEGORIES_COLLECTION,
        mq.LOCATIONS_COLLECTION,
    ]:
        coll.delete_many({})

    yield db

    # Clean collections after tests
    for coll in [
        mq.ITEMS_COLLECTION,
        mq.CATEGORIES_COLLECTION,
        mq.LOCATIONS_COLLECTION,
    ]:
        coll.delete_many({})


# -------------------- InventoryItem Tests --------------------
def test_insert_and_get_item():
    item = InventoryItem(
        name="Test Widget",
        quantity=10,
        category_id="testcat1",
        location_id="loc1",
        user_id="user1",
    )
    item_id = mq.insert_item(item)
    fetched = mq.get_item_by_id(item_id)

    assert fetched is not None
    assert fetched.name == "Test Widget"
    assert fetched.quantity == 10
    assert fetched.category_id == "testcat1"
    assert fetched.location_id == "loc1"


def test_update_item_name():
    item = InventoryItem(
        name="UpdateMe",
        quantity=5,
        category_id="testcat2",
        location_id="loc2",
        user_id="user2",
    )
    item_id = mq.insert_item(item)

    updated = mq.update_item(item_id, {"name": "UpdatedWidget"})
    assert updated.name == "UpdatedWidget"


def test_update_quantity():
    item = InventoryItem(
        name="QtyTest",
        quantity=5,
        category_id="cat3",
        location_id="loc3",
        user_id="user3",
    )
    item_id = mq.insert_item(item)

    updated = mq.update_quantity(item_id, 3)
    assert updated.quantity == 8


def test_delete_item():
    item = InventoryItem(
        name="DeleteMe",
        quantity=1,
        category_id="cat4",
        location_id="loc4",
        user_id="user4",
    )
    item_id = mq.insert_item(item)

    deleted = mq.delete_item(item_id)
    assert deleted is True
    assert mq.get_item_by_id(item_id) is None


# -------------------- Category Tests --------------------
def test_insert_and_get_category():
    cat = Category(name="Electronics")
    cat_id = mq.insert_category(cat)
    fetched = mq.get_category(cat_id)
    assert fetched is not None
    assert fetched.name == "Electronics"


# -------------------- Location Tests --------------------
def test_insert_and_get_location():
    loc = Location(name="Warehouse A")
    loc_id = mq.insert_location(loc)
    fetched = mq.get_location(loc_id)
    assert fetched is not None
    assert fetched.name == "Warehouse A"
