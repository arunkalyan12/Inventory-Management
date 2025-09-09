# components/inventory_management/cqrs/event_consumer.py
from components.inventory_management.db.mongo_queries import insert_inventory_for_user
from shared_utils.logging.logger import get_logger

logger = get_logger("event_consumer")


def handle_user_signed_up(user_id: str):
    """
    Handle the user_signed_up event in a monolith by creating default inventory for the user.
    """
    if not user_id:
        logger.warning("handle_user_signed_up called without user_id")
        return

    try:
        logger.info(f"Creating default inventory for user {user_id}")
        insert_inventory_for_user(user_id)
    except Exception as e:
        logger.exception(f"Failed to insert inventory for user {user_id}: {e}")
