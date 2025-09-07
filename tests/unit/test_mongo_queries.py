import pytest
from pymongo import MongoClient

from components.inventory_management.db import mongo_queries as mq
from components.inventory_management.db.models import (
    InventoryItem,
    Category,
    Location,
)


# ---- Test Setup ----
@pytest.fixture(scope="module")
def test_db():
    """
    Connect to a test database (not production).
    """
    client = MongoClient("mongodb://localhost:27017")
    db = client["test_inventory_db"]

    # Override collections in mongo_queries.py to point at test DB
    mq.ITEMS_COLLECTION = db["items"]
    mq.CATEGORIES_COLLECTION = db["categories"]
    mq.LOCATIONS_COLLECTION = db["locations"]

    # Clean before and after tests
    for coll in [
        mq.ITEMS_COLLECTION,
        mq.CATEGORIES_COLLECTION,
        mq.LOCATIONS_COLLECTION,
    ]:
        coll.delete_many({})

    yield db

    for coll in [
        mq.ITEMS_COLLECTION,
        mq.CATEGORIES_COLLECTION,
        mq.LOCATIONS_COLLECTION,
    ]:
        coll.delete_many({})


# ---- Tests ----
def test_insert_and_get_item(test_db):
    item = InventoryItem(
        name="Test Widget", quantity=10, category_id="testcat1", location_id="loc1"
    )
    item_id = mq.insert_item(item)
    fetched = mq.get_item_by_id(item_id)

    assert fetched is not None
    assert fetched.name == "Test Widget"
    assert fetched.quantity == 10


def test_update_tem(test_db):
    item = InventoryItem(
        name="updateMe", quantity=5, category_id="testcat2", location_id="loc2"
    )
    item_id = mq.insert_item(item)

    updated = mq.update_item(item_id, {"name": "UodatedWidget"})
    assert updated.name == "UodatedWidget"


def test_update_quantity(test_db):
    item = InventoryItem(
        name="QtyTest", quantity=5, category_id="cat3", location_id="loc3"
    )
    item_id = mq.insert_item(item)

    updated = mq.update_quantity(item_id, 3)
    assert updated.quantity == 8


def test_delete_item(test_db):
    item = InventoryItem(
        name="DeleteMe", quantity=1, category_id="cat4", location_id="loc4"
    )
    item_id = mq.insert_item(item)

    deleted = mq.delete_item(item_id)
    assert deleted is True
    assert mq.get_item_by_id(item_id) is None


def test_insert_and_get_category(test_db):
    cat = Category(name="Electronics")
    cat_id = mq.insert_category(cat)
    fetched = mq.get_category(cat_id)
    assert fetched.name == "Electronics"


def test_insert_and_get_location(test_db):
    loc = Location(name="Warehouse A")
    loc_id = mq.insert_location(loc)
    fetched = mq.get_location(loc_id)
    assert fetched.name == "Warehouse A"
