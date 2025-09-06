import os
from datetime import datetime
from typing import Dict
from pymongo import MongoClient
from shared_utils.config.config_loader import ConfigLoader
from shared_utils.logging.logger import get_logger

logger = get_logger("events")

# Load environment file first (default to dev)
env_file = os.getenv("ENV_FILE", "../../config/environments/dev.env")
config_loader = ConfigLoader(env_file=env_file)

# Load Mongo config (path can be overridden via ENV variable)
mongo_config_file = os.getenv("MONGO_CONFIG", "../../config/database/mongo_config.yml")
mongo_loader = ConfigLoader(services_file=mongo_config_file)

mongo_config = mongo_loader.services_config.get("mongodb", {})

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

events_collection = db.get(COLLECTIONS.get("events", "events"))


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
