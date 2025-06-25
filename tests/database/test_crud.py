import pytest
import os
import tempfile
import pandas as pd
from database.connection import get_connection
from database.crud import *
from database.queries import queries


@pytest.fixture()
def temp_db_path():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as tmp:
        os.environ["DB_PATH"] = tmp.name

        # Cria o schema e dados
        with get_connection() as conn:
            with open("database/schemas.sql") as f:
                conn.executescript(f.read())
            with open("database/dev_db.sql") as f:
                conn.executescript(f.read())

        yield tmp.name


def test_fetch_all(temp_db_path):
    expected = [('A',), ('B',), ('C',)]
    query = queries['test_fetch_query']
    res = fetch_all(query, (1,))
    
    assert res == expected


def test_fetch_one(temp_db_path):
    expected = ('A',)
    query = queries['test_fetch_query']
    res = fetch_one(query, (1,))
    
    assert res == expected


def test_execute_query(temp_db_path):
    expected = ('Paris',)
    input_query = queries['test_execute_query_insert']
    execute_query(input_query)
    get_query = queries['test_execute_query_get']
    res = fetch_one(get_query)
    
    assert res == expected


def test_execute_many(temp_db_path):
    expected = [('Paris',), ('Paris',)]
    input_query = queries['test_execute_query_insert']
    execute_many(input_query, [(), ()])
    get_query = queries['test_execute_query_get']
    res = fetch_all(get_query)
    
    assert res == expected


def test_execute_with_pandas(temp_db_path):
    expected = ['Paris', 'Paris']
    input_query = queries['test_execute_query_insert']
    execute_many(input_query, [(), ()])
    get_query = queries['test_execute_query_get']
    res = execute_with_pandas(get_query)
    
    assert res['city'].to_list() == expected

@pytest.mark.parametrize(
        "query_key, params, expected",
        [
            ('get_all_countries', (), ['Brazil', 'France']),
            ('get_all_cities', {'country':'France'}, ['Dijon', 'Paris'])
        ]
)
def test_simple_queries(query_key, params, expected, temp_db_path):
    query = queries[query_key]
    res = fetch_all(query, params)
    res = [row[0] for row in res]
    assert res == expected


def test_query_get_models_from_city(temp_db_path):
    expected = [2025, 2011]
    query = queries['get_models_from_city']
    query = query.format(sort_by='data_year DESC')
    params = {'city': 'Belo Horizonte'}
    res = execute_with_pandas(query, params)
    assert res['data_year'].to_list() == expected