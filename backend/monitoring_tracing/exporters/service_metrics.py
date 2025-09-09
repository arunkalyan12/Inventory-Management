from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import random

# --- Define Prometheus metrics ---
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["service", "method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "Histogram of HTTP request durations",
    ["service", "endpoint"],
)

service_health = Gauge(
    "service_health_status", "Service health status (1=up, 0=down)", ["service"]
)

custom_events = Counter(
    "custom_service_events_total",
    "Custom events per service (e.g., items added, model inferences)",
    ["service", "event_type"],
)


# --- Example simulation: replace with real hooks into your service ---
def simulate_requests():
    services = ["computer_vision", "inventory_management", "notification_service"]

    for service in services:
        # Random request duration
        duration = random.uniform(0.05, 2.0)
        endpoint = "/predict" if service == "computer_vision" else "/items"

        # Update histogram
        http_request_duration_seconds.labels(
            service=service, endpoint=endpoint
        ).observe(duration)

        # Count request with random status
        status = random.choice([200, 200, 200, 500])  # bias towards success
        http_requests_total.labels(
            service=service,
            method="POST" if service == "computer_vision" else "GET",
            endpoint=endpoint,
            status=status,
        ).inc()

        # Service health: set all healthy for now
        service_health.labels(service=service).set(1)

        # Custom event example
        if service == "inventory_management":
            custom_events.labels(service=service, event_type="item_added").inc(
                random.randint(0, 2)
            )
        elif service == "computer_vision":
            custom_events.labels(service=service, event_type="model_inference").inc(
                random.randint(0, 5)
            )


if __name__ == "__main__":
    # Start HTTP server for Prometheus to scrape
    start_http_server(9200)  # Exposes /metrics on port 9200
    print("Service metrics exporter running on :9200/metrics")

    while True:
        simulate_requests()
        time.sleep(5)
