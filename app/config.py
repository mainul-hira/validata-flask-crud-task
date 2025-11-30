"""
Configuration classes for different environments.

We keep database connection and environment-specific settings here
so that the application factory can easily switch configurations.
"""

import os


class BaseConfig:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Disable SQLAlchemy event system overhead if not needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Configuration for local development using SQL Server in Docker."""
    DEBUG = True
    # SQL Server connection string using pyodbc + SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DB_URL",
        "",
    )
