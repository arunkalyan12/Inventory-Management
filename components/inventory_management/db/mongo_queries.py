from datetime import datetime, timezone
from typing import List, Optional

from bson.objectid import ObjectId
from models import Category, InventoryItem, Location
from pymongo import ReturnDocument
from shared_utils.config.config_loader import ConfigLoader

config_loader = ConfigLoader(
    services_file=r"../../shared_utils/shared_utils/config/inventory_config.yaml"
)

# Access inventory management config
im_config = config_loader.get_service("inventory_management")

MONGO_URI = im_config.get("mongodb", {}).get("uri")
MONGO_DB = im_config.get("mongodb", {}).get("db_name")

ITEMS_COLLECTION = im_config.get("mongodb", {}).get("collections", {}).get("items")
CATEGORIES_COLLECTION = (
    im_config.get("mongodb", {}).get("collections", {}).get("categories")
)
LOCATIONS_COLLECTION = (
    im_config.get("mongodb", {}).get("collections", {}).get("locations")
)


def insert_item(item: InventoryItem) -> str:
    result = ITEMS_COLLECTION.insert_one(item.to_dict())
    return str(result.inserted_id)


def get_item_by_id(item_id: str) -> Optional[InventoryItem]:
    doc = ITEMS_COLLECTION.find_one({"_id": ObjectId(item_id)})
    if doc:
        return InventoryItem(**doc)
    return None


def list_items(filter: dict = None) -> List[InventoryItem]:
    cursor = ITEMS_COLLECTION.find(filter or {})
    return [InventoryItem(**doc) for doc in cursor]


def update_item(item_id: str, update_data: dict) -> Optional[InventoryItem]:
    update_data["updated_at"] = datetime.now(timezone.utc)
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"id": ObjectId(item_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if doc:
        return InventoryItem(**doc)
    return None


def delete_item(item_id: str) -> bool:
    result = ITEMS_COLLECTION.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0


def update_quantity(item_id: str, delta: int) -> Optional[InventoryItem]:
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$inc": {"quantity": delta}, "$set": {"updated_at": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER,
    )
    if doc:
        return InventoryItem(**doc)
    return None


def get_items_by_category(category_id: str) -> List[InventoryItem]:
    """Get all items belonging to a category"""
    cursor = ITEMS_COLLECTION.find({"category_id": category_id})
    return [InventoryItem(**doc) for doc in cursor]


def item_exists(item_id: str) -> bool:
    return ITEMS_COLLECTION.count_documents({"_id": ObjectId(item_id)}, limit=1) > 0


def insert_category(category: Category) -> str:
    result = CATEGORIES_COLLECTION.insert_one(category.to_dict())
    return str(result.inserted_id)


def get_category(category_id: str) -> Optional[Category]:
    doc = CATEGORIES_COLLECTION.find_one({"_id": ObjectId(category_id)})
    if doc:
        return Category(**doc)
    return None


def insert_location(location: Location) -> str:
    result = LOCATIONS_COLLECTION.insert_one(location.to_dict())
    return str(result.inserted_id)


def get_location(location_id: str) -> Optional[Location]:
    doc = LOCATIONS_COLLECTION.find_one({"_id": ObjectId(location_id)})
    if doc:
        return Location(**doc)
    return None
