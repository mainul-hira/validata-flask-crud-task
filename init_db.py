import pyodbc
import os

from dotenv import load_dotenv

load_dotenv()

# Configuration
SERVER = "(local)"
DRIVER = "{ODBC Driver 18 for SQL Server}"
DB_NAME = os.getenv("DB_NAME")


def conn_str(database):
    """Build a connection string for a given database."""
    return (
        f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={database};"
        f"UID=SA;PWD={os.getenv('DB_PASS')};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )


# 1. Create database if it doesn't exist
CREATE_DB_SQL = f"""
IF DB_ID('{DB_NAME}') IS NULL
BEGIN
    CREATE DATABASE [{DB_NAME}];
END;
"""

with pyodbc.connect(conn_str("master"), autocommit=True) as conn:
    with conn.cursor() as cursor:
        cursor.execute(CREATE_DB_SQL)
        print(f"Ensured database '{DB_NAME}' exists.")

# 2. Create table if it doesn't exist
CREATE_TABLE_SQL = """
IF OBJECT_ID('dbo.banks', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.banks (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL,
        location NVARCHAR(255) NOT NULL
    );
END;
"""

with pyodbc.connect(conn_str(DB_NAME), autocommit=True) as conn:
    with conn.cursor() as cursor:
        cursor.execute(CREATE_TABLE_SQL)
        print("Ensured table 'dbo.banks' exists.")

print("Script finished.")
