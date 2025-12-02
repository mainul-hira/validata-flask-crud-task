"""
Configuration classes for different environments.

We keep database connection and environment-specific settings here
so that the application factory can easily switch configurations.
"""

import os
import urllib.parse


class BaseConfig:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Disable SQLAlchemy event system overhead if not needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Configuration for local development using SQL Server in Docker."""

    DEBUG = True
    # SQL Server connection string using pyodbc + SQLAlchemy
    # We construct the URI here to ensure the password is correctly URL-encoded
    _db_user = os.getenv("DB_USER", "sa")
    _db_pass = os.getenv("DB_PASS", "YourStrongPassw0rd")
    _db_server = os.getenv("DB_SERVER", "db")
    _db_name = os.getenv("DB_NAME", "BankDB")

    # URL-encode the password to handle special characters
    _encoded_pass = urllib.parse.quote_plus(_db_pass)

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{_db_user}:{_encoded_pass}@{_db_server}:1433/{_db_name}"
        "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    print(SQLALCHEMY_DATABASE_URI)


class TestingConfig(BaseConfig):
    """
    Configuration for tests.

    Use an in-memory SQLite database for tests.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
