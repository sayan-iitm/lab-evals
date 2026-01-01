"""
Configuration loader for environment variables and settings.
Uses python-dotenv and lru_cache for efficient, environment-agnostic config.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized application settings object."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
    GOOGLE_CLIENT_ID: str = os.getenv(
        "GOOGLE_CLIENT_ID", "your-google-client-id"
    )
    ENV: str = os.getenv("ENV", "development")


@lru_cache
def get_settings() -> Settings:
    return Settings()
