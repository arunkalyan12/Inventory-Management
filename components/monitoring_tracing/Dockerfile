# Use lightweight Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (curl for healthchecks/debug)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies (prometheus_client, pymongo, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy monitoring + tracing scripts
COPY prometheus/ ./prometheus/
COPY grafana/ ./grafana/
COPY tracing/ ./tracing/
COPY mq_metrics.py service_metrics.py ./

# Expose Prometheus metrics port
EXPOSE 8000

# Default command: run Python metric exporters
# (these expose /metrics endpoints that Prometheus scrapes)
CMD ["python", "-u", "service_metrics.py"]
