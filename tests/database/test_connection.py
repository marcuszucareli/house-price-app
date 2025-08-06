import pytest

def test_get_connection(temp_db_path):
    
    from database.connection import get_connection
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT 1")
        result = c.fetchone()
        assert result[0] == 1


