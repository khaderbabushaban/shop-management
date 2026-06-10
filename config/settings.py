"""
config/settings.py
------------------
Centralised application settings loaded from environment variables.
Create a .env file (see .env.example) before running the application.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file if it exists
load_dotenv()


def _require(key: str) -> str:
    """Return the value of an env variable, raising an error if it is missing."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Please copy .env.example to .env and fill in your values."
        )
    return value


class DatabaseConfig:
    """All database connection settings."""
    HOST: str = os.getenv("DB_HOST", "localhost")
    NAME: str = os.getenv("DB_NAME", "ShopManagement")
    USER: str = os.getenv("DB_USER", "postgres")
    PASSWORD: str = _require("DB_PASSWORD")
    SCHEMA: str = os.getenv("DB_SCHEMA", "db")
