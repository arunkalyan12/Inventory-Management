# components/inventory_management/Dockerfile

# ----------------------------
# 1. Base image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# 2. Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# 3. Copy requirements first (for caching)
# ----------------------------
COPY requirements.txt .

# ----------------------------
# 4. Install dependencies
# ----------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# 5. Copy the rest of the code
# ----------------------------
COPY . .

# ----------------------------
# 6. Expose the port
# ----------------------------
EXPOSE 8001

# ----------------------------
# 7. Copy dev.env into container and set env variable
# ----------------------------
# Adjust path according to your repo structure
COPY ../../config/environment/dev.env ./config/environment/dev.env
ENV ENV_FILE=/app/config/environment/dev.env

# ----------------------------
# 8. Default command to run the service
# ----------------------------
CMD ["uvicorn", "components.inventory_management.api.app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
