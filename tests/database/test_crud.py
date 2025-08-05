import pytest
from database.queries import queries


def test_fetch_all(temp_db_path):
    expected = [('A',), ('B',), ('C',)]
    query = queries['test_fetch_query']

    from database.crud import fetch_all

    res = fetch_all(query, (1,))
    
    assert res == expected


def test_fetch_one(temp_db_path):
    expected = ('A',)
    query = queries['test_fetch_query']

    from database.crud import fetch_one

    res = fetch_one(query, (1,))
    
    assert res == expected


def test_execute_query(temp_db_path):
    expected = ('Paris',)
    input_query = queries['test_execute_query_insert']

    from database.crud import execute_query, fetch_one

    execute_query(input_query)
    get_query = queries['test_execute_query_get']
    res = fetch_one(get_query)
    
    assert res == expected


def test_execute_many(temp_db_path):
    expected = [('Paris',), ('Paris',)]
    input_query = queries['test_execute_query_insert']

    from database.crud import execute_many, fetch_all

    execute_many(input_query, [(), ()])
    get_query = queries['test_execute_query_get']
    res = fetch_all(get_query)
    
    assert res == expected


def test_execute_with_pandas(temp_db_path):
    expected = ['Paris', 'Paris']
    input_query = queries['test_execute_query_insert']
    
    from database.crud import execute_many, execute_with_pandas

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

    from database.crud import fetch_all

    query = queries[query_key]
    res = fetch_all(query, params)
    res = [row[0] for row in res]
    assert res == expected


def test_query_get_models_from_city(temp_db_path):
    expected = [2025, 2011]
    query = queries['get_models_from_city']
    query = query.format(sort_by='data_year DESC')
    params = {'city': 'Belo Horizonte'}

    from database.crud import execute_with_pandas

    res = execute_with_pandas(query, params)
    assert res['data_year'].to_list() == expected