"""
Pytest fixtures for setting up the Flask application and database
for tests.
"""

import os
import sys
import pytest

# Ensure project root (parent of tests/) is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app, db  # noqa: E402
from app.config import TestingConfig  # noqa: E402


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
