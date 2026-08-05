import psycopg
from config import Config


def get_connection():
    """
    Creates and returns a connection to the Lakebase database.
    """

    connection = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
    )

    return connection
