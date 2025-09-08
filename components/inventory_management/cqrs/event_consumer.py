import json
from components.shared_utils.message_queue import mq_client
from components.inventory_management.db.mongo_queries import insert_inventory_for_user


def callback(ch, method, properties, body):
    """
    Called whenever a new message is received from RabbitMQ.
    Listens for 'user_signed_up' events and creates default inventory records for the user.
    """
    event = json.loads(body)

    if event.get("type") == "user_signed_up":
        user_id = event["payload"]["user_id"]
        print(f"[Inventory Service] Creating default inventory for user {user_id}")
        insert_inventory_for_user(user_id)

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """
    Start consuming messages from the exchange.
    """
    conn = mq_client.create_consuming_connection()
    channel = conn.channel()
    channel.exchange_declare(
        exchange=mq_client.EVENT_EXCHANGE, exchange_type="fanout", durable=True
    )

    # Temporary exclusive queue for this consumer
    result = channel.queue_declare(queue="", exclusive=True, durable=False)
    queue_name = result.method.queue
    channel.queue_bind(exchange=mq_client.EVENT_EXCHANGE, queue=queue_name)

    print("[Inventory Service] Listening for user_signed_up events...")
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False
    )
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
