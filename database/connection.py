import sqlite3
import os
from contextlib import contextmanager


@contextmanager
def get_connection():
    DB_PATH = os.getenv('DB_PATH')
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
