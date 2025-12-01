# Validata Flask CRUD Task

A Flask application demonstrating CRUD operations for "Bank" records. It includes both a server-side rendered HTML interface and a REST API, backed by a SQL Server database.

## Prerequisites

- **Python 3.13+**
- **Docker** (for running SQL Server on macOS/Linux)

## Database Setup

Since macOS does not natively support Microsoft SQL Server, we use Docker to run it.

1.  **Run SQL Server 2022 container:**

    ```bash
    docker pull mcr.microsoft.com/mssql/server:2022-latest

    docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Password" \
    -p 1433:1433 --name sql_server \
    -d mcr.microsoft.com/mssql/server:2022-latest
    ```

    *Note: Replace `Password` with a strong password of your choice.*

2.  **Configure Environment Variables:**

    Create a `.env` file in the project root (copy from `.env.example`) and set your database connection string, database name, database password, and secret key:

    ```bash
    # .env
    SECRET_KEY=dev-secret-key
    DB_USER=sa
    DB_NAME=BankDB
    DB_PASS=
    DB_URL=mssql+pyodbc://${DB_USER}:${DB_PASS}@localhost:1433/${DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server
    ```

    *Ensure you have the ODBC Driver 18 for SQL Server installed on your machine.*

## Installation

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
    or you can create the database and tables manually using the following SQL commands:

    ```sql
    CREATE DATABASE master;
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

## Running the Application

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Flask development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

- **Home / Bank List:** `http://127.0.0.1:5000`
- **API Endpoint:** `http://127.0.0.1:5000/api/banks`

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