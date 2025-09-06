from prometheus_client import Gauge, Counter, start_http_server
import time
import random  # replace with actual queue client
from shared_utils.message_queue.mq_client import MQClient

# --- Define Prometheus metrics ---
queue_backlog = Gauge("mq_queue_backlog", "Number of messages in the queue", ["queue"])
messages_consumed = Counter(
    "mq_messages_consumed_total", "Total messages consumed", ["queue"]
)
messages_published = Counter(
    "mq_messages_published_total", "Total messages published", ["queue"]
)


def collect_metrics():
    """
    Collects queue stats and updates Prometheus metrics.
    Replace the mock logic with real RabbitMQ/Kafka queries.
    """
    mq = MQClient()  # Your wrapper around pika/kafka-python
    queues = ["inventory_events", "cv_events", "notification_events"]

    for q in queues:
        # Example: fetch queue depth (backlog)
        backlog = mq.get_queue_backlog(q)  # must return int
        queue_backlog.labels(queue=q).set(backlog)

        # Example: update counters (you'd hook this into consume/publish logic)
        messages_consumed.labels(queue=q).inc(random.randint(0, 5))
        messages_published.labels(queue=q).inc(random.randint(0, 5))


if __name__ == "__main__":
    # Start HTTP server for Prometheus to scrape
    start_http_server(9100)  # Exposes /metrics on port 9100
    print("MQ metrics exporter running on :9100/metrics")

    # Loop forever, updating metrics
    while True:
        collect_metrics()
        time.sleep(5)
