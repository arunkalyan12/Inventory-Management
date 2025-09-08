# components/inventory_management/api/event_listener.py
import json
import time
from components.shared_utils.message_queue import mq_client
from components.inventory_management.db.mongo_queries import insert_inventory_for_user
from shared_utils.logging.logger import get_logger

logger = get_logger("event_listener")

# We'll keep the connection and channel references so we can close them on shutdown
_conn = None
_channel = None


def _on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        event_type = message.get("type") or message.get("event_type")
        payload = message.get("payload") or {}

        logger.info(f"MQ event received: {event_type} payload={payload}")

        if event_type == "user_signed_up":
            user_id = payload.get("user_id")
            if user_id:
                logger.info(f"Creating default inventory for user {user_id}")
                try:
                    insert_inventory_for_user(user_id)
                except Exception as e:
                    logger.exception(
                        f"Failed insert_inventory_for_user for {user_id}: {e}"
                    )
            else:
                logger.warning("user_signed_up event missing user_id")
        else:
            logger.debug(f"Ignored event type: {event_type}")
    except json.JSONDecodeError:
        logger.exception("Failed to decode MQ message")
    except Exception:
        logger.exception("Unhandled exception in MQ callback")
    finally:
        # If using manual ack, ack here. But we rely on auto_ack=False below
        try:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            pass


def start_listener_blocking(retry_delay: int = 5):
    """
    Blocking call that starts consuming on a temporary queue bound to the shared exchange.
    Designed to run in a background thread or startup event.
    """
    global _conn, _channel
    while True:
        try:
            _conn = mq_client.create_consuming_connection()
            _channel = _conn.channel()
            _channel.exchange_declare(
                exchange=mq_client.EVENT_EXCHANGE, exchange_type="fanout", durable=True
            )

            # Create an exclusive queue for this consumer instance (unique temporary queue)
            result = _channel.queue_declare(queue="", exclusive=True, durable=False)
            queue_name = result.method.queue

            _channel.queue_bind(exchange=mq_client.EVENT_EXCHANGE, queue=queue_name)

            logger.info("Inventory event listener started and waiting for messages...")
            # Use manual acking to avoid losing messages on crash; callback will ack after processing.
            _channel.basic_consume(
                queue=queue_name, on_message_callback=_on_message, auto_ack=False
            )
            _channel.start_consuming()  # Blocking
        except Exception as e:
            logger.exception(
                f"Listener connection error: {e}. Reconnecting in {retry_delay}s..."
            )
            try:
                if _conn:
                    _conn.close()
            except Exception:
                pass
            time.sleep(retry_delay)


def stop_listener():
    """
    Stop consuming and close connection. Safe to call from shutdown event.
    """
    try:
        if _channel and _channel.is_open:
            _channel.stop_consuming()
    except Exception:
        pass
    try:
        if _conn and _conn.is_open:
            _conn.close()
    except Exception:
        pass
