"""
Application factory for the Flask app.

This module creates and configures the Flask application instance.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app(config_class):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import models so SQLAlchemy knows them
    from . import models  # noqa: F401

    # Register blueprints (HTML views and REST API)
    from .api import api_bp
    from .routes import bank_bp

    app.register_blueprint(bank_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app