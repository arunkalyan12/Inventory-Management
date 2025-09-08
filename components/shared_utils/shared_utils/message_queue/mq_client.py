# components/shared_utils/message_queue/mq_client.py
import os
import json
import threading
from typing import Callable
from pathlib import Path

import pika
from dotenv import load_dotenv

# Load environment (adjust path if necessary)
load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[4] / "config/environment/dev.env"
)  # expects dev.env in repo root or env already exported

MQ_HOST = os.getenv("EVENT_QUEUE_HOST", os.getenv("MQ_HOST", "localhost"))
MQ_PORT = int(os.getenv("EVENT_QUEUE_PORT", os.getenv("MQ_PORT", 5672)))
MQ_USER = os.getenv("MQ_USER", "guest")
MQ_PASS = os.getenv("MQ_PASS", "guest")
EVENT_EXCHANGE = os.getenv(
    "EVENT_QUEUE_NAME", "inventory_events"
)  # used as exchange name

_credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
_parameters = pika.ConnectionParameters(
    host=MQ_HOST,
    port=MQ_PORT,
    credentials=_credentials,
    heartbeat=600,
    blocked_connection_timeout=300,
)


def publish_event(event_type: str, payload: dict) -> None:
    """
    Publish an event to the shared exchange. Lightweight (opens/closes connection per publish).
    Used by auth service after signup/login events.
    """
    message = json.dumps({"type": event_type, "payload": payload})
    connection = pika.BlockingConnection(_parameters)
    try:
        channel = connection.channel()
        # Use a durable fanout exchange so consumers bind a queue and all receive events
        channel.exchange_declare(
            exchange=EVENT_EXCHANGE, exchange_type="fanout", durable=True
        )
        channel.basic_publish(
            exchange=EVENT_EXCHANGE,
            routing_key="",
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )  # persistent
    finally:
        connection.close()


def create_consuming_connection() -> pika.BlockingConnection:
    """
    Returns a new BlockingConnection for consumers (long-running).
    """
    return pika.BlockingConnection(_parameters)


# Helper to run consumer in separate thread if desired (utility)
def run_consumer_in_thread(target: Callable, *args, **kwargs) -> threading.Thread:
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread
