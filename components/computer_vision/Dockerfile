# Use official PyTorch image with CUDA support (change CUDA version as needed)
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire computer_vision code folder into the container
COPY . .

# Set environment variable for MLflow tracking URI
ENV MLFLOW_TRACKING_URI=http://your-mlflow-server:8080

# Default command to start training
CMD ["python", "train_yolo.py"]
