import pytest
import json
from database.client import Database
from database.create_db import model_columns
from tempfile import TemporaryDirectory

@pytest.fixture(scope="module")
def get_test_db():
    table_name = 'models'
    with TemporaryDirectory() as tmpdir:
        database_path = f"{tmpdir}/database.db"
        database = Database(database_path)
        yield database_path, database, table_name


def test_Database(get_test_db):
    database_path, database, table_name = get_test_db
    assert database.database_path == database_path


def test_create_table(get_test_db):
    database_path, database, table_name = get_test_db
    database.create_table(table_name, model_columns)
    database.c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' " \
        f"AND name='{table_name}'")
    assert database.c.fetchone() is not None


def test_insert_data(get_test_db):
    data = {
    'id': "ABC123",
    'flavor': "sklearn",
    'r2': .1962,
    'mae': 1963,
    'mape': .2002,
    'rmse': .2004,
    'algorithm': "Random forest",
    'data_year': 2011,
    'country': "Brazil",
    'cities': json.dumps(["Santos", "São Paulo"],),
    'author': "Giovanni Silva de Oliveira"
    }
    database_path, database, table_name = get_test_db
    database.insert_data('models', data)
    database.c.execute(f"SELECT * FROM {table_name} WHERE id='ABC123'")
    assert database.c.fetchone() is not None


def test_get_data(get_test_db):
    database_path, database, table_name = get_test_db
    condition = "id='ABC123'"
    df = database.get_data(table_name, condition)
    df = df.set_index('id')
    assert len(df) == 1
    assert df.loc['ABC123']['country'] == "Brazil"


def test_delete_data(get_test_db):
    database_path, database, table_name = get_test_db
    condition = "id='ABC123'"
    database.delete_data(table_name, condition)
    database.c.execute(f"SELECT * FROM {table_name} WHERE id='ABC123'")
    assert database.c.fetchone() is None
