# shared_utils/logging/logger.py
import logging
import sys
from pathlib import Path

def get_logger(service_name: str, log_file: str = None):
    """
    Creates and returns a logger with a consistent format.

    Args:
        service_name (str): Name of the service (e.g., "computer_vision")
        log_file (str, optional): Path to log file. If None, logs only to console.

    Returns:
        logging.Logger: Configured logger
    """

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)  # Can be overridden via env variable

    # Prevent adding multiple handlers if logger already configured
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter: clear and easy to read
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
