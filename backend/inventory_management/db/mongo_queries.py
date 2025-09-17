import os
from datetime import datetime, timezone
from typing import List, Optional
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from .models import (
    InventoryItem,
    Category,
    Location,
    User,
    ShoppingListItem,
)
from shared_utils.logging.logger import get_logger
from dotenv import load_dotenv
from pathlib import Path

# Load dev.env from repo root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / "dev.env")

logger = get_logger("mongo_queries")

# -------------------- MongoDB Connection --------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_NAME = os.getenv("DB_NAME", "inventory_db")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")

if DB_USER and DB_PASS:
    MONGO_URI = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
else:
    MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# -------------------- Collections --------------------
ITEMS_COLLECTION = db["items"]
CATEGORIES_COLLECTION = db["categories"]
LOCATIONS_COLLECTION = db["locations"]
USERS_COLLECTION = db["users"]
SHOPPING_LIST_COLLECTION = db["shopping_lists"]


# -------------------- Inventory --------------------
def insert_item(item: InventoryItem) -> str:
    result = ITEMS_COLLECTION.insert_one(item.to_dict())
    logger.info(
        f"Inserted inventory item: {item.name} for user {item.user_id} with ID {result.inserted_id}"
    )
    return str(result.inserted_id)


def insert_inventory_for_user(user_id: str):
    """
    Insert default inventory items for a specific user.
    """
    now = datetime.utcnow()
    default_items = [
        InventoryItem(
            user_id=user_id,
            name="Sample Item 1",
            quantity=10,
            created_at=now,
            updated_at=now,
        ).to_dict(),
        InventoryItem(
            user_id=user_id,
            name="Sample Item 2",
            quantity=5,
            created_at=now,
            updated_at=now,
        ).to_dict(),
    ]
    result = ITEMS_COLLECTION.insert_many(default_items)
    logger.info(
        f"[Inventory] Inserted {len(result.inserted_ids)} default items for user {user_id}"
    )


def get_item_by_id(item_id: str) -> Optional[InventoryItem]:
    doc = ITEMS_COLLECTION.find_one({"_id": ObjectId(item_id)})
    return InventoryItem(**doc) if doc else None


def list_items(filter: dict = None) -> List[InventoryItem]:
    cursor = ITEMS_COLLECTION.find(filter or {})
    return [InventoryItem(**doc) for doc in cursor]


def update_item(item_id: str, update_data: dict) -> Optional[InventoryItem]:
    update_data["updated_at"] = datetime.now(timezone.utc)
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    return InventoryItem(**doc) if doc else None


def delete_item(item_id: str) -> bool:
    result = ITEMS_COLLECTION.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0


def update_quantity(item_id: str, delta: int) -> Optional[InventoryItem]:
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$inc": {"quantity": delta}, "$set": {"updated_at": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER,
    )
    return InventoryItem(**doc) if doc else None


def get_items_by_category(category_id: str) -> List[InventoryItem]:
    cursor = ITEMS_COLLECTION.find({"category_id": category_id})
    return [InventoryItem(**doc) for doc in cursor]


def item_exists(item_id: str) -> bool:
    return ITEMS_COLLECTION.count_documents({"_id": ObjectId(item_id)}, limit=1) > 0


# -------------------- Batch Inventory Insert --------------------
def add_inventory_batch(items: list[dict], user_id: str = None) -> list[dict]:
    """
    Inserts multiple inventory items at once.

    Args:
        items (list[dict]): List of inventory items. Each item should have keys:
            - name (str)
            - quantity (int)
            - category_id (str, optional)
            - confidence (float, optional)
        user_id (str, optional): User ID to associate items with

    Returns:
        List[dict]: Inserted items with '_id' included
    """
    if not items:
        logger.info("No items provided for batch insert.")
        return []

    now = datetime.utcnow()
    items_to_insert = []

    for item in items:
        item_doc = {
            "name": item.get("name"),
            "quantity": item.get("quantity", 1),
            "category_id": item.get("category_id"),
            "created_at": now,
            "updated_at": now,
        }
        if user_id:
            item_doc["user_id"] = user_id
        # Optional fields from CV predictions
        if "confidence" in item:
            item_doc["confidence"] = item["confidence"]
        items_to_insert.append(item_doc)

    result = ITEMS_COLLECTION.insert_many(items_to_insert)
    logger.info(f"Inserted {len(result.inserted_ids)} items in batch.")

    # Return inserted items with MongoDB _id
    inserted_items = []
    for item_doc, _id in zip(items_to_insert, result.inserted_ids):
        item_doc["_id"] = str(_id)
        inserted_items.append(item_doc)

    return inserted_items


# -------------------- Categories --------------------
def insert_category(category: Category) -> str:
    result = CATEGORIES_COLLECTION.insert_one(category.to_dict())
    return str(result.inserted_id)


def get_category(category_id: str) -> Optional[Category]:
    doc = CATEGORIES_COLLECTION.find_one({"_id": ObjectId(category_id)})
    return Category(**doc) if doc else None


# -------------------- Locations --------------------
def insert_location(location: Location) -> str:
    result = LOCATIONS_COLLECTION.insert_one(location.to_dict())
    return str(result.inserted_id)


def get_location(location_id: str) -> Optional[Location]:
    doc = LOCATIONS_COLLECTION.find_one({"_id": ObjectId(location_id)})
    return Location(**doc) if doc else None


# -------------------- Users --------------------
def insert_user(user: User) -> str:
    result = USERS_COLLECTION.insert_one(user.to_dict())
    logger.info(f"Inserted user: {user.email} with ID {result.inserted_id}")
    return str(result.inserted_id)


def get_user_by_email(email: str) -> Optional[User]:
    doc = USERS_COLLECTION.find_one({"email": email})
    return User(**doc) if doc else None


def get_user_by_id(user_id: str) -> Optional[User]:
    doc = USERS_COLLECTION.find_one({"_id": ObjectId(user_id)})
    return User(**doc) if doc else None


def list_users(filter: dict = None) -> List[User]:
    cursor = USERS_COLLECTION.find(filter or {})
    return [User(**doc) for doc in cursor]


# -------------------- Shopping List --------------------
def insert_shopping_item(item: ShoppingListItem) -> str:
    result = SHOPPING_LIST_COLLECTION.insert_one(item.to_dict())
    logger.info(
        f"Inserted shopping list item: {item.item_name} for user {item.user_id}"
    )
    return str(result.inserted_id)


def get_shopping_list(user_id: str) -> List[ShoppingListItem]:
    cursor = SHOPPING_LIST_COLLECTION.find({"user_id": user_id})
    return [ShoppingListItem(**doc) for doc in cursor]


def get_shopping_item_by_id(item_id: str) -> Optional[ShoppingListItem]:
    doc = SHOPPING_LIST_COLLECTION.find_one({"_id": ObjectId(item_id)})
    return ShoppingListItem(**doc) if doc else None


def list_shopping_items(filter: dict = None) -> List[ShoppingListItem]:
    cursor = SHOPPING_LIST_COLLECTION.find(filter or {})
    return [ShoppingListItem(**doc) for doc in cursor]


def update_shopping_item(item_id: str, update_data: dict) -> Optional[ShoppingListItem]:
    doc = SHOPPING_LIST_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    return ShoppingListItem(**doc) if doc else None


def delete_shopping_item(item_id: str) -> bool:
    result = SHOPPING_LIST_COLLECTION.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0


def clear_inventory():
    """
    Deletes all documents in the inventory collection.
    Useful for testing or resetting the DB.
    """
    result = ITEMS_COLLECTION.delete_many({})
    logger.info(f"Cleared {result.deleted_count} items from inventory.")
    return result.deleted_count
