# shared_utils/config/config_loader.py
import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

class ConfigLoader:
    """
    Loads environment variables and YAML configuration files.
    Provides a simple interface to access them.
    """

    def __init__(self, env_file: str = None, services_file: str = None):
        """
        Initialize the loader.

        Args:
            env_file (str, optional): Path to .env file
            services_file (str, optional): Path to services.yml
        """
        # Load environment variables from .env file if given
        if env_file:
            env_path = Path(env_file)
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
            else:
                print(f"[ConfigLoader] Warning: {env_file} not found. Using system env variables.")

        # Load services YAML if provided
        self.services_config = {}
        if services_file:
            services_path = Path(services_file)
            if services_path.exists():
                with open(services_path, "r") as f:
                    self.services_config = yaml.safe_load(f)
            else:
                print(f"[ConfigLoader] Warning: {services_file} not found.")

    def get_env(self, key: str, default=None):
        """
        Get an environment variable. Returns default if not set.
        """
        return os.getenv(key, default)

    def get_service(self, service_name: str):
        """
        Get the dictionary of config for a specific service from services.yml
        """
        return self.services_config.get("services", {}).get(service_name, {})
