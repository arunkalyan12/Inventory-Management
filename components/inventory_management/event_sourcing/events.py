from datetime import datetime
from typing import Dict

from shared_utils.config.config_loader import ConfigLoader

config_loader = ConfigLoader(
    services_file=r"../../shared_utils/shared_utils/config/inventory_config.yaml"
)

# Access inventory management config
im_config = config_loader.get_service("inventory_management")

client = im_config.get("mongodb", {}).get("uri")
db = im_config.get("mongodb", {}).get("db_name")

events_collection = db["events"]


def record_event(event_type: str, payload: Dict):
    """Record an event in MongoDB"""
    event_doc = {"type": event_type, "payload": payload, "timestamp": datetime.utcnow()}
    events_collection.insert_one(event_doc)


# Optional: Event classes for type clarity
class ItemCreated:
    type = "ItemCreated"


class ItemUpdated:
    type = "ItemUpdated"


class ItemDeleted:
    type = "ItemDeleted"


class QuantityUpdated:
    type = "QuantityUpdated"
