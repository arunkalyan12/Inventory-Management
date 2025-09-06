from typing import Dict
from shared_utils.config.config_loader import ConfigLoader
from shared_utils.logging.logger import get_logger

from components.inventory_management.db.models import InventoryItem
from components.inventory_management.db.mongo_queries import (
    delete_item,
    insert_item,
    update_item,
    update_quantity,
)
from components.inventory_management.event_sourcing.events import record_event

logger = get_logger("comands")

config_loader = ConfigLoader(
    services_file=r"../../shared_utils/shared_utils/config/inventory_config.yaml"
)


def create_item(item_data: Dict) -> str:
    """Create a new inventory item and record event."""
    try:
        item = InventoryItem(**item_data)
        logger.debug(f"Creating item with data: {item_data}")
        item_id = insert_item(item)
        logger.info(f"Item created with ID: {item_id}")
        record_event("ItemCreated", {"item_id": item_id, **item_data})
        logger.debug(f"Event recorded for item creation: {item_id}")
        return item_id
    except Exception as e:
        logger.error(f"Failed to create item: {item_data}, error: {e}", exc_info=True)
        raise


def update_inventory_item(item_id: str, update_data: Dict):
    """Update item fields and record event."""
    try:
        logger.debug(f"Updating item {item_id} with data: {update_data}")
        updated_item = update_item(item_id, update_data)
        if updated_item:
            logger.info(f"Item updated successfully: {item_id}")
            record_event(
                "ItemUpdated", {"item_id": item_id, "updated_fields": update_data}
            )
            logger.debug(f"Event recorded for item update: {item_id}")
        else:
            logger.warning(f"Item not found for update: {item_id}")
        return updated_item
    except Exception as e:
        logger.error(
            f"Failed to update item {item_id} with data {update_data}: {e}",
            exc_info=True,
        )
        raise


def delete_inventory_item(item_id: str):
    """Delete item and record event."""
    try:
        logger.debug(f"Deleting item: {item_id}")
        success = delete_item(item_id)
        if success:
            logger.info(f"Item deleted successfully: {item_id}")
            record_event("ItemDeleted", {"item_id": item_id})
            logger.debug(f"Event recorded for item deletion: {item_id}")
        else:
            logger.warning(f"Item not found for deletion: {item_id}")
        return success
    except Exception as e:
        logger.error(f"Failed to delete item {item_id}: {e}", exc_info=True)
        raise


def change_item_quantity(item_id: str, delta: int):
    """Increment/decrement quantity and record event."""
    try:
        logger.debug(f"Changing quantity for item {item_id} by {delta}")
        updated_item = update_quantity(item_id, delta)
        if updated_item:
            logger.info(f"Quantity updated for item {item_id} by {delta}")
            record_event("QuantityUpdated", {"item_id": item_id, "delta": delta})
            logger.debug(f"Event recorded for quantity update: {item_id}")
        else:
            logger.warning(f"Item not found for quantity update: {item_id}")
        return updated_item
    except Exception as e:
        logger.error(
            f"Failed to change quantity for item {item_id} by {delta}: {e}",
            exc_info=True,
        )
        raise
