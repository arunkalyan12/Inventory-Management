from shared_utils.config.config_loader import ConfigLoader

from components.inventory_management.db.mongo_queries import (
    delete_item,
    insert_item,
    update_item,
    update_quantity,
)

config_loader = ConfigLoader(
    services_file=r"../../shared_utils/shared_utils/config/inventory_config.yaml"
)

# Access inventory management config
im_config = config_loader.get_service("inventory_management")

client = im_config.get("mongodb", {}).get("uri")
db_name = im_config.get("mongodb", {}).get("db_name")
db = client[db_name]

events_collection = db["events"]


def apply_event(event: dict) -> None:
    """Apply a single event to the inventory."""
    event_type = event["type"]
    payload = event["payload"]

    if event_type == "ItemCreated":
        # Avoid duplicates if already exists
        if not insert_item(payload):
            insert_item(payload)

    elif event_type == "ItemUpdated":
        update_item(payload["item_id"], payload["updated_fields"])

    elif event_type == "ItemDeleted":
        delete_item(payload["item_id"])

    elif event_type == "QuantityUpdated":
        update_quantity(payload["item_id"], payload["delta"])


def replay_all_events() -> None:
    """Rebuild entire inventory from all events."""
    cursor = events_collection.find().sort("timestamp", 1)
    for event in cursor:
        apply_event(event)


def replay_item(item_id: str) -> None:
    """Rebuild a single item from its events."""
    cursor = events_collection.find({"payload.item_id": item_id}).sort("timestamp", 1)
    for event in cursor:
        apply_event(event)
