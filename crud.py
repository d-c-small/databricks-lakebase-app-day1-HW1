from lakebase import get_cursor

_VALID_STATUSES = frozenset({"open", "in_progress", "resolved"})


def get_ticket_stats():
    with get_cursor() as cur:
        cur.execute(
            "SELECT status, COUNT(*) AS count FROM tickets GROUP BY status"
        )
        rows = cur.fetchall()
    stats = {"open": 0, "in_progress": 0, "resolved": 0}
    for row in rows:
        if row["status"] in stats:
            stats[row["status"]] = int(row["count"])
    return stats


def get_all_tickets(status_filter=None):
    with get_cursor() as cur:
        if status_filter in _VALID_STATUSES:
            cur.execute(
                """
                SELECT ticket_id, title, status, created_by, created_at
                FROM tickets
                WHERE status = %s
                ORDER BY created_at DESC
                """,
                (status_filter,),
            )
        else:
            cur.execute(
                """
                SELECT ticket_id, title, status, created_by, created_at
                FROM tickets
                ORDER BY created_at DESC
                """
            )
        return cur.fetchall()


def get_ticket_by_id(ticket_id):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT ticket_id, title, status, created_by, created_at
            FROM tickets
            WHERE ticket_id = %s
            """,
            (ticket_id,),
        )
        return cur.fetchone()


def get_messages_for_ticket(ticket_id):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT message_id, ticket_id, message_text, author, created_at
            FROM ticket_messages
            WHERE ticket_id = %s
            ORDER BY created_at ASC
            """,
            (ticket_id,),
        )
        return cur.fetchall()


def create_ticket(title, created_by):
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO tickets (title, status, created_by, created_at)
            VALUES (%s, 'open', %s, NOW())
            RETURNING ticket_id
            """,
            (title, created_by),
        )
        return cur.fetchone()[0]


def add_message_to_ticket(ticket_id, message_text, author):
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO ticket_messages (ticket_id, message_text, author, created_at)
            VALUES (%s, %s, %s, NOW())
            """,
            (ticket_id, message_text, author),
        )


def update_ticket_status(ticket_id, new_status):
    with get_cursor() as cur:
        cur.execute(
            "UPDATE tickets SET status = %s WHERE ticket_id = %s",
            (new_status, ticket_id),
        )


def delete_ticket(ticket_id):
    with get_cursor() as cur:
        # Delete messages first to satisfy the foreign key constraint
        cur.execute(
            "DELETE FROM ticket_messages WHERE ticket_id = %s", (ticket_id,)
        )
        cur.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id,))
