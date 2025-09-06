import os
from shared_utils.logging.logger import get_logger

logger = get_logger("predict")

MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "")
