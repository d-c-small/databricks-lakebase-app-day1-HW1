from psycopg.extras import RealDictCursor
from database import get_connection


def get_all_tickets():
    """
    Retrieves all support tickets from the database.
    """

    connection = get_connection()

    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            ticket_id,
            title,
            status,
            created_by,
            created_at
        FROM tickets
        ORDER BY created_at DESC;
    """)

    tickets = cursor.fetchall()

    cursor.close()
    connection.close()

    return tickets
