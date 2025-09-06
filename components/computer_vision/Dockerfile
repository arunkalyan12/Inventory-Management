# Dockerfile.inference
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget unzip libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary inference code
COPY model/ ./model/
COPY utils/ ./utils/
COPY inference.py .
COPY api/ ./api/

# Pull latest model weights from remote storage (S3, GCS, MinIO, etc.)
# Example using AWS CLI:
# RUN aws s3 cp s3://my-model-bucket/model_weights.pt ./model/weights/model_weights.pt
# Or fetch during container startup
COPY download_weights.sh .
RUN chmod +x download_weights.sh

# Expose port for API
EXPOSE 8000

# Start API (FastAPI/Uvicorn example)
CMD ["sh", "-c", "./download_weights.sh && uvicorn api.main:app --host 0.0.0.0 --port 8000"]
