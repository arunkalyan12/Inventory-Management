import os
from shared_utils.config.config_loader import ConfigLoader
from shared_utils.logging.logger import get_logger
from pymongo import MongoClient
from components.inventory_management.db.mongo_queries import (
    delete_item,
    insert_item,
    update_item,
    update_quantity,
)

logger = get_logger("replay")

# Load environment file first (defaults to dev)
env_file = os.getenv("ENV_FILE", "../../config/environments/dev.env")
config_loader = ConfigLoader(env_file=env_file)

# Each .env sets MONGO_CONFIG path
mongo_config_file = os.getenv("MONGO_CONFIG", "../../config/database/mongo_config.yml")

# Load mongo config
mongo_loader = ConfigLoader(services_file=mongo_config_file)
full_config = mongo_loader.services_config
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
events_collection = db["events"]


def apply_event(event: dict) -> None:
    """Apply a single event to the inventory with logging."""
    event_type = event["type"]
    payload = event["payload"]

    try:
        logger.debug(f"Applying event {event_type} with payload: {payload}")

        if event_type == "ItemCreated":
            if not insert_item(payload):
                insert_item(payload)
            logger.info(f"ItemCreated applied for item_id: {payload.get('item_id')}")

        elif event_type == "ItemUpdated":
            update_item(payload["item_id"], payload["updated_fields"])
            logger.info(f"ItemUpdated applied for item_id: {payload.get('item_id')}")

        elif event_type == "ItemDeleted":
            delete_item(payload["item_id"])
            logger.info(f"ItemDeleted applied for item_id: {payload.get('item_id')}")

        elif event_type == "QuantityUpdated":
            update_quantity(payload["item_id"], payload["delta"])
            logger.info(
                f"QuantityUpdated applied for item_id: {payload.get('item_id')} with delta {payload.get('delta')}"
            )

        else:
            logger.warning(f"Unknown event type: {event_type}")

    except Exception as e:
        logger.error(
            f"Failed to apply event {event_type} with payload {payload}: {e}",
            exc_info=True,
        )
        raise


def replay_all_events() -> None:
    """Rebuild entire inventory from all events with logging."""
    try:
        logger.info("Replaying all events...")
        cursor = events_collection.find().sort("timestamp", 1)
        for event in cursor:
            apply_event(event)
        logger.info("All events replayed successfully.")
    except Exception as e:
        logger.error(f"Failed to replay all events: {e}", exc_info=True)
        raise


def replay_item(item_id: str) -> None:
    """Rebuild a single item from its events with logging."""
    try:
        logger.info(f"Replaying events for item_id: {item_id}")
        cursor = events_collection.find({"payload.item_id": item_id}).sort(
            "timestamp", 1
        )
        for event in cursor:
            apply_event(event)
        logger.info(f"All events replayed for item_id: {item_id}")
    except Exception as e:
        logger.error(
            f"Failed to replay events for item_id {item_id}: {e}", exc_info=True
        )
        raise
