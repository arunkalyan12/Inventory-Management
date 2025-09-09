# shared_utils/logging/logger.py
import logging
import sys
import os
from pathlib import Path


def get_logger(service_name: str):
    """
    Creates and returns a logger with a consistent format.
    - Dev/Test: logs to console + ./logs/{service_name}.log
    - Prod: logs only to console (Kubernetes handles aggregation)
    """

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Which environment?
    env = os.getenv("APP_ENV", "dev").lower()

    # Formatter: clear and easy to read
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (always on)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (only for dev/test)
    if env in ("dev", "test"):
        log_file = f"./logs/{service_name}.log"
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
