import os
from dotenv import load_dotenv
from pathlib import Path

# Load dev.env from root/config/environment/dev.env
env_path = Path(__file__).resolve().parents[3] / "config/environment/dev.env"
load_dotenv(dotenv_path=env_path)

# General settings
PROJECT_NAME = os.getenv("PROJECT_NAME", "inventory-management-system")
ENV = os.getenv("ENV", "dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# MongoDB settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_NAME = os.getenv("DB_NAME", "inventory_db")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")

# Authentication / JWT
JWT_SECRET = os.getenv(
    "JWT_SECRET", "15d8a8d55656ac3421cb936ea502d556ca365b743a01520b3c69b05abf4e5d9d"
)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day by default

# Inventory API settings
IM_API_HOST = os.getenv("IM_API_HOST", "0.0.0.0")
IM_API_PORT = int(os.getenv("IM_API_PORT", 8001))

# Logging
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/inventory.log")
