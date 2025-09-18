# ----------------------------
# 1️⃣ Base image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# 2️⃣ Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# 3️⃣ Install system dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 4️⃣ Copy requirements and install Python dependencies
# ----------------------------
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# 5️⃣ Copy backend source code
# ----------------------------
COPY backend/ ./

# ----------------------------
# 6️⃣ Create directories for models, data, logs
# ----------------------------
RUN mkdir -p /app/model /app/data/train /app/data/valid /app/logs

# ----------------------------
# 7️⃣ Expose API port
# ----------------------------
EXPOSE 8000

# ----------------------------
# 8️⃣ Set default environment variables (optional)
# ----------------------------
ENV ENV=dev \
    LOG_LEVEL=DEBUG \
    MODEL_PATH=/app/model/model_weights.pt \
    TRAIN_DATA_PATH=/app/data/train \
    VALID_DATA_PATH=/app/data/valid \
    LOG_FILE_PATH=/app/logs/backend.log

# ----------------------------
# 9️⃣ Start FastAPI app with Uvicorn
# ----------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
