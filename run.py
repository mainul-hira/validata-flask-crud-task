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
    # Use host='0.0.0.0' to make the server accessible from outside the container
    app.run(host="0.0.0.0", port=5001, debug=True)
