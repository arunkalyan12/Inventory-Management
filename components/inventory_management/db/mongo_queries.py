from datetime import datetime, timezone
import os
from typing import List, Optional

from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument

from models import Category, InventoryItem, Location
from shared_utils.config.config_loader import ConfigLoader
from shared_utils.logging.logger import get_logger

logger = get_logger("mq")

# Load environment file first (defaults to dev)
env_file = os.getenv("ENV_FILE", "../../config/environments/dev.env")
config_loader = ConfigLoader(env_file)

# Each .env sets MONGO_CONFIG path
mongo_config_file = os.getenv("MONGO_CONFIG", "../../config/database/mongo_config.yml")

# Load mongo config
mongo_loader = ConfigLoader(services_file=mongo_config_file)
full_config = config_loader.services_config
mongo_config = full_config.get("mongodb", {})

MONGO_URI = mongo_config.get("uri")
MONGO_DB = mongo_config.get("db_name")
COLLECTIONS = mongo_config.get("collections", {})

# Connect to MongoDB
client = MongoClient(
    MONGO_URI,
    username=mongo_config.get("username"),
    password=mongo_config.get("password"),
    authSource=mongo_config.get("authSource", "admin"),
    maxPoolSize=mongo_config.get("maxPoolSize", 50),
    minPoolSize=mongo_config.get("minPoolSize", 5),
    serverSelectionTimeoutMS=mongo_config.get("serverSelectionTimeoutMS", 5000),
    ssl=mongo_config.get("ssl", False),
)

db = client[MONGO_DB]

# Collections
ITEMS_COLLECTION = db[COLLECTIONS.get("items", "items")]
CATEGORIES_COLLECTION = db[COLLECTIONS.get("categories", "categories")]
LOCATIONS_COLLECTION = db[COLLECTIONS.get("locations", "locations")]


def insert_item(item: InventoryItem) -> str:
    try:
        result = ITEMS_COLLECTION.insert_one(item.to_dict())
        logger.info(f"Inserted item {item.name} with ID {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Failed to insert item {item.name}: {e}")
        raise


def get_item_by_id(item_id: str) -> Optional[InventoryItem]:
    logger.debug(f"Fetching item by ID: {item_id}")
    doc = ITEMS_COLLECTION.find_one({"_id": ObjectId(item_id)})
    if doc:
        logger.info(f"Item found: {item_id}")
        return InventoryItem(**doc)
    else:
        logger.warning(f"Item not found: {item_id}")
        return None


def list_items(filter: dict = None) -> List[InventoryItem]:
    logger.debug(f"Listing items with filter: {filter}")
    cursor = ITEMS_COLLECTION.find(filter or {})
    items = [InventoryItem(**doc) for doc in cursor]
    logger.info(f"Found {len(items)} items")
    return items


def update_item(item_id: str, update_data: dict) -> Optional[InventoryItem]:
    logger.debug(f"Updating item {item_id} with data: {update_data}")
    update_data["updated_at"] = datetime.now(timezone.utc)
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if doc:
        logger.info(f"Item updated: {item_id}")
        return InventoryItem(**doc)
    else:
        logger.warning(f"Failed to update, item not found: {item_id}")
        return None


def delete_item(item_id: str) -> bool:
    logger.debug(f"Deleting item: {item_id}")
    result = ITEMS_COLLECTION.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count > 0:
        logger.info(f"Item deleted: {item_id}")
        return True
    else:
        logger.warning(f"Failed to delete, item not found: {item_id}")
        return False


def update_quantity(item_id: str, delta: int) -> Optional[InventoryItem]:
    logger.debug(f"Updating quantity for item {item_id} by {delta}")
    doc = ITEMS_COLLECTION.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$inc": {"quantity": delta}, "$set": {"updated_at": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER,
    )
    if doc:
        logger.info(f"Quantity updated for item {item_id}")
        return InventoryItem(**doc)
    else:
        logger.warning(f"Failed to update quantity, item not found: {item_id}")
        return None


def get_items_by_category(category_id: str) -> List[InventoryItem]:
    logger.debug(f"Fetching items by category: {category_id}")
    cursor = ITEMS_COLLECTION.find({"category_id": category_id})
    items = [InventoryItem(**doc) for doc in cursor]
    logger.info(f"Found {len(items)} items for category {category_id}")
    return items


def item_exists(item_id: str) -> bool:
    logger.debug(f"Checking if item exists: {item_id}")
    exists = ITEMS_COLLECTION.count_documents({"_id": ObjectId(item_id)}, limit=1) > 0
    logger.info(f"Item {item_id} exists: {exists}")
    return exists


def insert_category(category: Category) -> str:
    logger.debug(f"Inserting category: {category.name}")
    result = CATEGORIES_COLLECTION.insert_one(category.to_dict())
    logger.info(f"Category inserted with ID: {result.inserted_id}")
    return str(result.inserted_id)


def get_category(category_id: str) -> Optional[Category]:
    logger.debug(f"Fetching category by ID: {category_id}")
    doc = CATEGORIES_COLLECTION.find_one({"_id": ObjectId(category_id)})
    if doc:
        logger.info(f"Category found: {category_id}")
        return Category(**doc)
    else:
        logger.warning(f"Category not found: {category_id}")
        return None


def insert_location(location: Location) -> str:
    logger.debug(f"Inserting location: {location.name}")
    result = LOCATIONS_COLLECTION.insert_one(location.to_dict())
    logger.info(f"Location inserted with ID: {result.inserted_id}")
    return str(result.inserted_id)


def get_location(location_id: str) -> Optional[Location]:
    logger.debug(f"Fetching location by ID: {location_id}")
    doc = LOCATIONS_COLLECTION.find_one({"_id": ObjectId(location_id)})
    if doc:
        logger.info(f"Location found: {location_id}")
        return Location(**doc)
    else:
        logger.warning(f"Location not found: {location_id}")
        return None
