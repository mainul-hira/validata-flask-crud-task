"""
Entry point for running the application.

This file imports the create_app factory and uses the DevelopmentConfig to connect to the SQL Server via Docker when running locally.
"""

from app import create_app
from app.config import DevelopmentConfig

# Create the app with development configuration
app = create_app(DevelopmentConfig)


if __name__ == "__main__":
    # Run the development server
    app.run(debug=True)