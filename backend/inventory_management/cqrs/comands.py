from typing import Dict
from shared_utils.logging.logger import get_logger

from components.inventory_management.db.models import (
    InventoryItem,
    User,
    ShoppingListItem,
)
from components.inventory_management.db.mongo_queries import (
    delete_item,
    insert_item,
    update_item,
    update_quantity,
    insert_user,
    update_user,
    insert_shopping_item,
    update_shopping_item,
    delete_shopping_item,
)
from components.inventory_management.event_sourcing.events import record_event

logger = get_logger("commands")

# ------------------- Inventory Commands -------------------


def create_item(item_data: Dict) -> str:
    try:
        item = InventoryItem(**item_data)
        logger.debug(f"Creating item with data: {item_data}")
        item_id = insert_item(item)
        logger.info(f"Item created with ID: {item_id}")
        record_event("ItemCreated", {"item_id": item_id, **item_data})
        return item_id
    except Exception as e:
        logger.error(f"Failed to create item: {item_data}, error: {e}", exc_info=True)
        raise


def update_inventory_item(item_id: str, update_data: Dict):
    try:
        logger.debug(f"Updating item {item_id} with data: {update_data}")
        updated_item = update_item(item_id, update_data)
        if updated_item:
            logger.info(f"Item updated successfully: {item_id}")
            record_event(
                "ItemUpdated", {"item_id": item_id, "updated_fields": update_data}
            )
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
    try:
        logger.debug(f"Deleting item: {item_id}")
        success = delete_item(item_id)
        if success:
            logger.info(f"Item deleted successfully: {item_id}")
            record_event("ItemDeleted", {"item_id": item_id})
        else:
            logger.warning(f"Item not found for deletion: {item_id}")
        return success
    except Exception as e:
        logger.error(f"Failed to delete item {item_id}: {e}", exc_info=True)
        raise


def change_item_quantity(item_id: str, delta: int):
    try:
        logger.debug(f"Changing quantity for item {item_id} by {delta}")
        updated_item = update_quantity(item_id, delta)
        if updated_item:
            logger.info(f"Quantity updated for item {item_id} by {delta}")
            record_event("QuantityUpdated", {"item_id": item_id, "delta": delta})
        else:
            logger.warning(f"Item not found for quantity update: {item_id}")
        return updated_item
    except Exception as e:
        logger.error(
            f"Failed to change quantity for item {item_id} by {delta}: {e}",
            exc_info=True,
        )
        raise


# ------------------- User Commands -------------------


def create_user(user_data: Dict) -> str:
    try:
        user = User(**user_data)
        user_id = insert_user(user)
        logger.info(f"User created with ID: {user_id}")
        return user_id
    except Exception as e:
        logger.error(f"Failed to create user: {user_data}, error: {e}", exc_info=True)
        raise


def update_user_info(user_id: str, update_data: Dict):
    try:
        updated_user = update_user(user_id, update_data)
        if updated_user:
            logger.info(f"User updated successfully: {user_id}")
        else:
            logger.warning(f"User not found for update: {user_id}")
        return updated_user
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}", exc_info=True)
        raise


# ------------------- Shopping List Commands -------------------


def add_shopping_item(item_data: Dict) -> str:
    try:
        item = ShoppingListItem(**item_data)
        item_id = insert_shopping_item(item)
        logger.info(f"Shopping list item added with ID: {item_id}")
        return item_id
    except Exception as e:
        logger.error(
            f"Failed to add shopping item: {item_data}, error: {e}", exc_info=True
        )
        raise


def update_shopping_list_item(item_id: str, update_data: Dict):
    try:
        updated_item = update_shopping_item(item_id, update_data)
        if updated_item:
            logger.info(f"Shopping item updated: {item_id}")
        else:
            logger.warning(f"Shopping item not found for update: {item_id}")
        return updated_item
    except Exception as e:
        logger.error(f"Failed to update shopping item {item_id}: {e}", exc_info=True)
        raise


def remove_shopping_list_item(item_id: str):
    try:
        success = delete_shopping_item(item_id)
        if success:
            logger.info(f"Shopping item removed: {item_id}")
        else:
            logger.warning(f"Shopping item not found for deletion: {item_id}")
        return success
    except Exception as e:
        logger.error(f"Failed to remove shopping item {item_id}: {e}", exc_info=True)
        raise
