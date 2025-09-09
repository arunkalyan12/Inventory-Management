import os
from datetime import datetime
from typing import Dict
from pymongo import MongoClient
from shared_utils.logging.logger import get_logger
from dotenv import load_dotenv
from pathlib import Path

# Load dev.env from repo root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / "dev.env")

logger = get_logger("events")

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


def record_event(event_type: str, payload: Dict):
    """Record an event in MongoDB with logging."""
    try:
        event_doc = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow(),
        }
        result = events_collection.insert_one(event_doc)
        logger.info(f"Event recorded: {event_type} with ID {result.inserted_id}")
    except Exception as e:
        logger.error(
            f"Failed to record event {event_type} with payload {payload}: {e}",
            exc_info=True,
        )
        raise
