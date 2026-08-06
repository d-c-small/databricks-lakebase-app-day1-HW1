import os
from contextlib import contextmanager
import psycopg


def _get_connection_url() -> str:
    # LAKEBASE_URL is injected at runtime from the secret defined in app.yaml
    url = os.environ.get("LAKEBASE_URL")
    if not url:
        raise RuntimeError(
            "LAKEBASE_URL is not set. Verify the resources.secrets binding in app.yaml."
        )
    return url


@contextmanager
def get_cursor(row_factory=None):
    """Yields a cursor; commits on success, rolls back on error, and always closes the connection.

    psycopg3's `with conn:` only commits/rollbacks — it never closes. This wrapper
    ensures the connection is always returned to Lakebase after each operation.
    """
    kwargs = {"row_factory": row_factory} if row_factory is not None else {}
    conn = psycopg.connect(_get_connection_url(), **kwargs)
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
