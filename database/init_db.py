import os
from database.connection import get_connection

DB_PATH = os.getenv('DB_PATH')


def is_intiated() -> bool:

    with get_connection() as conn:
        c = conn.cursor()

        c.execute(
            "SELECT name FROM sqlite_master " \
            "WHERE type='table' AND name='cities'")
        table_exists = c.fetchone() is not None

        if not table_exists:
            return table_exists, False

        c.execute("SELECT COUNT(*) FROM cities")
        total = c.fetchone()[0]
        has_data = total > 0
        return table_exists, has_data


def init_db(
        schema_path="database/schemas.sql",
        data_path="database/dev_db.sql"):
    table_exists, has_data = is_intiated()
    is_dev = True if os.getenv('ENV') == 'dev' else False
    
    # Exclude previous dev db
    if is_dev:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            table_exists= False
            has_data= False

    if not table_exists:
        with open(schema_path) as f:
            schema = f.read()

        with get_connection() as conn:
            c = conn.cursor()
            c.executescript(schema)

            if not has_data and is_dev:
                with open(data_path) as f:
                    data = f.read()
                c.executescript(data)


init_db()