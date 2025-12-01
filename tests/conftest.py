"""
Pytest fixtures for setting up the Flask application and database
for tests.
"""

import pytest

from app import create_app, db
from app.config import TestingConfig


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test session.

    We use the TestingConfig which points to an in-memory SQLite DB.
    """
    app = create_app(TestingConfig)

    # Create tables before tests
    with app.app_context():
        db.create_all()

    yield app

    # Drop everything after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Flask test client for making HTTP requests in tests.
    """
    return app.test_client()
