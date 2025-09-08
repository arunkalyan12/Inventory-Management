# components/inventory_management/event_sourcing/replay.py
import os
from pymongo import MongoClient
from shared_utils.logging.logger import get_logger
from components.inventory_management.db.mongo_queries import (
    delete_item,
    insert_item,
    update_item,
    update_quantity,
)
from dotenv import load_dotenv
from pathlib import Path

# Load dev.env from repo root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / "dev.env")

logger = get_logger("replay")

# -------------------- MongoDB Connection from dev.env --------------------
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

events_collection = db["events"]  # default collection name


# -------------------- Event Replay Functions --------------------
def apply_event(event: dict) -> None:
    """Apply a single event to the inventory with logging."""
    event_type = event["type"]
    payload = event["payload"]

    try:
        logger.debug(f"Applying event {event_type} with payload: {payload}")

        if event_type == "ItemCreated":
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
