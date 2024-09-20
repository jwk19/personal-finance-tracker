import psycopg2
from psycopg2 import sql

# Database connection parameters (update these with your actual database credentials)
DB_NAME = "finance_db"
DB_USER = "james"
DB_PASSWORD = "Secure@sql"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise