# shared_utils/config/config_loader.py
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pymongo import MongoClient


class ConfigLoader:
    """
    Loads environment variables and YAML configuration files.
    Provides a simple interface to access them.
    """

    def __init__(
        self, env_file: str = None, services_file: str = None, mongo_file: str = None
    ):
        """
        Initialize the loader.

        Args:
            env_file (str, optional): Path to .env file
            services_file (str, optional): Path to services.yml
            mongo_file (str, optional): Path to mongo_config.yml
        """
        # Load environment variables from .env file if given
        if env_file:
            env_path = Path(env_file)
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
            else:
                print(
                    f"[ConfigLoader] Warning: {env_file} not found. Using system env variables."
                )

        # Load services YAML if provided
        self.services_config = {}
        if services_file:
            services_path = Path(services_file)
            if services_path.exists():
                with open(services_path, "r") as f:
                    self.services_config = yaml.safe_load(f)
            else:
                print(f"[ConfigLoader] Warning: {services_file} not found.")

        # Load mongo YAML if provided
        self.mongo_config = {}
        if mongo_file:
            mongo_path = Path(mongo_file)
            if mongo_path.exists():
                with open(mongo_path, "r", encoding="utf-8") as f:
                    self.mongo_config = yaml.safe_load(f)
            else:
                print(f"[ConfigLoader] Warning: {mongo_file} not found.")

    def get_env(self, key: str, default=None):
        """Get an environment variable. Returns default if not set."""
        return os.getenv(key, default)

    def get_service(self, service_name: str):
        """Get the dictionary of config for a specific service from services.yml"""
        return self.services_config.get("services", {}).get(service_name, {})

    def get_mongo_client(self):
        """Build and return a MongoClient using mongo_config.yml + env overrides."""
        if not self.mongo_config:
            raise ValueError("[ConfigLoader] MongoDB config not loaded")

        mongo_cfg = self.mongo_config.get("mongo", {})

        username = os.getenv("MONGO_USER", mongo_cfg.get("username"))
        password = os.getenv("MONGO_PASS", mongo_cfg.get("password"))
        host = mongo_cfg.get("host", "mongodb://localhost:27017")

        # Build full URI with optional auth
        if username and password and "@" not in host:
            uri = host.replace("mongodb://", f"mongodb://{username}:{password}@")
        else:
            uri = host

        client = MongoClient(
            uri,
            authSource=mongo_cfg.get("authSource", "admin"),
            maxPoolSize=mongo_cfg.get("maxPoolSize", 50),
            minPoolSize=mongo_cfg.get("minPoolSize", 5),
            serverSelectionTimeoutMS=mongo_cfg.get("serverSelectionTimeoutMS", 5000),
            tls=mongo_cfg.get("ssl", False),
            replicaSet=mongo_cfg.get("replicaSet") or None,
        )

        return client

    def get_mongo_db(self):
        """Helper to directly return the Mongo database instance."""
        client = self.get_mongo_client()
        db_name = self.mongo_config.get("mongo", {}).get("database", "inventory_db")
        return client[db_name]
