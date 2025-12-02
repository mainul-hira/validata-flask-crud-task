# Validata Flask CRUD Task

A Flask application demonstrating CRUD operations for "Bank" records. It includes both a server-side rendered HTML interface and a REST API, backed by a SQL Server database.

## Prerequisites

- **Python 3.13+** (for local development)
- **Docker** and **Docker Compose** (for containerized deployment)

## Running with Docker (Recommended)

The easiest way to run this application is using Docker Compose, which will set up both the Flask application and SQL Server database automatically.

> **Note on Docker Compose Versions:**  
> This guide uses Docker Compose V2 syntax (`docker compose`). If you have Docker Compose V1 installed, replace `docker compose` with `docker-compose` (with a hyphen) in all commands below.

### Quick Start

1.  **Clone the repository and navigate to the project directory:**

    ```bash
    cd /path/to/validata-flask-crud-task
    ```

2.  **Start the application:**

    ```bash
    docker compose up -d
    ```

    This command will:
    - Pull the SQL Server 2022 image
    - Build the Flask application image
    - Create and start both containers
    - Initialize the database automatically

3.  **Access the application:**

    - **Web Interface:** `http://127.0.0.1:5001`
    - **API Endpoint:** `http://127.0.0.1:5001/api/banks`

4.  **View logs:**

    ```bash
    docker compose logs -f
    ```

5.  **Stop the application:**

    ```bash
    docker compose down
    ```

    To remove volumes (delete database data):
    ```bash
    docker compose down -v
    ```

### Docker Environment Configuration

The application uses a `.env.docker` file for environment variables. For production, you should:

1. Copy `.env.docker` to create your own environment file
2. Change the SQL Server password (`DB_PASS` and update in `docker-compose.yml` for the `db` service)
3. Update the `SECRET_KEY` environment variable
4. Update the `DB_URL` connection string accordingly

### Useful Docker Commands

```bash
# Rebuild the Flask app after code changes
docker compose up -d --build

# Run tests inside the container
docker compose exec web pytest

# Access the Flask container shell
docker compose exec web bash

# A Python script `client_api.py` is provided to demonstrate interacting with the REST API programmatically. To run it first access the Flask container shell and then run the script:

```bash
docker compose exec web bash
python client_api.py

# Access SQL Server with sqlcmd
docker compose exec db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrongPassw0rd

# View container status
docker compose ps

# Remove all containers and volumes
docker compose down -v
```


---

## Local Development Setup (Without Docker)

### Database Setup (Local Development)

Since macOS does not natively support Microsoft SQL Server, we use Docker to run it locally.

1.  **Run SQL Server 2022 container:**

    ```bash
    docker pull mcr.microsoft.com/mssql/server:2022-latest

    docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourStrongPassw0rd" \
    -p 1433:1433 --name sql_server \
    -d mcr.microsoft.com/mssql/server:2022-latest
    ```

    *Note: Replace `YourStrongPassw0rd` with a strong password of your choice.*

2.  **Configure Environment Variables:**

    Create a `.env` file in the project root (copy from `.env.example`) and set your database connection string, database name, database password, and secret key:

    ```bash
    # .env
    SECRET_KEY=dev-secret-key
    DB_USER=sa
    DB_NAME=BankDB
    DB_PASS=YourStrongPassw0rd
    DB_URL=mssql+pyodbc://${DB_USER}:${DB_PASS}@localhost:1433/${DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server
    ```

    *Ensure you have the ODBC Driver 18 for SQL Server installed on your machine.*


### Installation (Local Development)

1.  **Create and activate a virtual environment:**
    create a virtual environment in the root directory of the project where the `run.py` file is located.
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**

    you can use a script `python init_db.py` to initialize the database.
    if this script not working, please install this on mac 
    ```
    brew install unixodbc 
    brew list msodbcsql18
    If that errors, install it:
    brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
    brew update
    ACCEPT_EULA=Y brew install msodbcsql18

    ```
    after installing these, run the script again `python init_db.py`

    or you can create the database and tables manually using the following SQL commands:

    ```sql
    CREATE DATABASE BankDB;
    ``` 

    then run the following SQL commands to create the tables:

    ```sql
    USE BankDB;
    CREATE TABLE banks (
        id INT PRIMARY KEY IDENTITY(1,1),
        name NVARCHAR(255) NOT NULL,
        location NVARCHAR(255) NOT NULL
    );
    ``` 


### Running the Application (Local Development)

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Flask development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5001`.

- **Home / Bank List:** `http://127.0.0.1:5001`
- **API Endpoint:** `http://127.0.0.1:5001/api/banks`

## Running Tests

This project uses `pytest` for testing. It uses an in-memory SQLite database for fast, isolated tests.

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run all tests:

```bash
pytest
```

## Client API Script

A Python script `client_api.py` is provided to demonstrate interacting with the REST API programmatically.

Ensure the Flask app is running in one terminal (`python run.py`), then run the client script in another terminal:

```bash
python client_api.py
```

This script will perform a sequence of operations: List, Create, Get Detail, Update, and Delete banks via the API.

## Project Structure

The application logic is separated into two main blueprints:

-   **`app/routes.py` (HTML Interface):**
    -   Handles browser requests.
    -   Returns HTML using Jinja2 templates (`app/templates/`).
    -   Supports form submissions for creating and editing banks.
    -   Uses `flash` messages for user feedback.

-   **`app/api.py` (REST API):**
    -   Handles API requests (prefixed with `/api`).
    -   Returns JSON responses.
    -   Implements standard REST methods (GET, POST, PUT, DELETE).
    -   Includes custom error handling to return JSON errors instead of HTML error pages.