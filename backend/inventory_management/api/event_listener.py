# backend/inventory_management/api/event_listener.py

from backend.inventory_management.db.mongo_queries import insert_inventory_for_user
from shared_utils.logging.logger import get_logger
import time

logger = get_logger("event_listener")

# Global flag to control the listener
_listening = True


def start_listener_blocking():
    """
    Start a blocking listener that simulates handling events.
    """
    logger.info("Event listener started.")
    try:
        while _listening:
            # Simulate listening for 'user_signed_up' event every 5 seconds
            time.sleep(5)
            example_user_id = "user_123"
            logger.info(f"Simulating 'user_signed_up' event for {example_user_id}")
            handle_user_signed_up(example_user_id)
    except Exception as e:
        logger.exception(f"Event listener error: {e}")
    finally:
        logger.info("Event listener stopped.")


def stop_listener():
    """
    Stop the listener gracefully.
    """
    global _listening
    logger.info("Stopping event listener...")
    _listening = False


def handle_user_signed_up(user_id: str):
    """
    Handle user signup event by creating default inventory.
    """
    if not user_id:
        logger.warning("handle_user_signed_up called without user_id")
        return

    try:
        logger.info(f"Creating default inventory for user {user_id}")
        insert_inventory_for_user(user_id)
    except Exception as e:
        logger.exception(f"Failed to insert inventory for {user_id}: {e}")
