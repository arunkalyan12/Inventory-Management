from ..db.mongo_queries import (
    insert_item, update_item, delete_item, update_quantity
)
from ..event_sourcing.events import record_event
from ..db.models import InventoryItem
from typing import Dict
from shared_utils.config.config_loader import ConfigLoader

config_loader = ConfigLoader(services_file=r"../../shared_utils/shared_utils/config/inventory_config.yaml")


def create_item(item_data: Dict) -> str:
    """Create a new inventory item and record event"""
    item = InventoryItem(**item_data)
    item_id = insert_item(item)
    record_event("ItemCreated", {"item_id": item_id, **item_data})
    return item_id


def update_inventory_item(item_id: str, update_data: Dict):
    """Update item fields and record event"""
    updated_item = update_item(item_id, update_data)
    if updated_item:
        record_event("ItemUpdated", {"item_id": item_id, "updated_fields": update_data})
    return updated_item


def delete_inventory_item(item_id: str):
    """Delete item and record event"""
    success = delete_item(item_id)
    if success:
        record_event("ItemDeleted", {"item_id": item_id})
    return success


def change_item_quantity(item_id: str, delta: int):
    """Increment/decrement quantity and record event"""
    updated_item = update_quantity(item_id, delta)
    if updated_item:
        record_event("QuantityUpdated", {"item_id": item_id, "delta": delta})
    return updated_item
