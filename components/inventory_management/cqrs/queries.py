from components.inventory_management.db.mongo_queries import (
    get_item_by_id,
    get_items_by_category,
    list_items,
    get_user_by_id,
    list_users,
    get_shopping_item_by_id,
    list_shopping_items,
)
from shared_utils.logging.logger import get_logger

logger = get_logger("queries")

# ------------------- Inventory Queries -------------------


def get_item(item_id: str):
    """Fetch a single item by ID."""
    try:
        logger.debug(f"Fetching item with ID: {item_id}")
        item = get_item_by_id(item_id)
        if item:
            logger.info(f"Item found: {item_id}")
        else:
            logger.warning(f"Item not found: {item_id}")
        return item
    except Exception as e:
        logger.error(f"Failed to fetch item {item_id}: {e}", exc_info=True)
        raise


def list_all_items(filters: dict = None):
    """List all items optionally filtered by a dict."""
    try:
        logger.debug(f"Listing all items with filters: {filters}")
        items = list_items(filters)
        logger.info(f"Returned {len(items)} items")
        return items
    except Exception as e:
        logger.error(f"Failed to list items with filters {filters}: {e}", exc_info=True)
        raise


def list_items_by_category(category_id: str):
    """List all items for a specific category."""
    try:
        logger.debug(f"Fetching items by category: {category_id}")
        items = get_items_by_category(category_id)
        logger.info(f"Found {len(items)} items for category {category_id}")
        return items
    except Exception as e:
        logger.error(
            f"Failed to fetch items for category {category_id}: {e}", exc_info=True
        )
        raise


# ------------------- User Queries -------------------


def get_user(user_id: str):
    """Fetch a single user by ID."""
    try:
        logger.debug(f"Fetching user with ID: {user_id}")
        user = get_user_by_id(user_id)
        if user:
            logger.info(f"User found: {user_id}")
        else:
            logger.warning(f"User not found: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Failed to fetch user {user_id}: {e}", exc_info=True)
        raise


def list_all_users(filters: dict = None):
    """List all users optionally filtered by a dict."""
    try:
        logger.debug(f"Listing all users with filters: {filters}")
        users = list_users(filters)
        logger.info(f"Returned {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Failed to list users with filters {filters}: {e}", exc_info=True)
        raise


# ------------------- Shopping List Queries -------------------


def get_shopping_item(item_id: str):
    """Fetch a single shopping list item by ID."""
    try:
        logger.debug(f"Fetching shopping item with ID: {item_id}")
        item = get_shopping_item_by_id(item_id)
        if item:
            logger.info(f"Shopping item found: {item_id}")
        else:
            logger.warning(f"Shopping item not found: {item_id}")
        return item
    except Exception as e:
        logger.error(f"Failed to fetch shopping item {item_id}: {e}", exc_info=True)
        raise


def list_all_shopping_items(filters: dict = None):
    """List all shopping list items optionally filtered by a dict."""
    try:
        logger.debug(f"Listing all shopping items with filters: {filters}")
        items = list_shopping_items(filters)
        logger.info(f"Returned {len(items)} shopping items")
        return items
    except Exception as e:
        logger.error(
            f"Failed to list shopping items with filters {filters}: {e}", exc_info=True
        )
        raise
