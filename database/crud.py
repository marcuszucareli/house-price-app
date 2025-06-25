import pandas as pd
from database.connection import get_connection

def fetch_all(query, params=()):
    with get_connection() as conn:
        c = conn.execute(query, params)
        return c.fetchall()


def fetch_one(query, params=()):
    with get_connection() as conn:
        c = conn.execute(query, params)
        return c.fetchone()


def execute_query(query, params=()):
    with get_connection() as conn:
        conn.execute(query, params)


def execute_many(query, param_list):
    with get_connection() as conn:
        conn.executemany(query, param_list)


def execute_with_pandas(query, params=()):
    with get_connection() as conn:
        res = pd.read_sql_query(query, params=params, con=conn)
        return res