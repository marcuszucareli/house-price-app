import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def get_connection():
    DB_PATH = os.getenv('DB_PATH')
    dir_path = Path(DB_PATH).parent
    dir_path.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
