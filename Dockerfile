# Use Python 3.11 slim image as base (Debian Bookworm - more stable)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ODBC Driver 18 for SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get install -y unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Expose port 5001
EXPOSE 5001

# Run the Flask development server
CMD ["python", "run.py"]
