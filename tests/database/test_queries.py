import pytest
import pandas as pd
from tempfile import TemporaryDirectory
from database.client import Database
from database.queries import *



@pytest.fixture(scope="module")
def get_test_db():

    model_records = [
        {
            'id': "A",
            'flavor': "sklearn",
            'r2': .1962,
            'mae': 1963,
            'mape': .2002,
            'rmse': .2004,
            'algorithm': "Random forest",
            'data_year': 2011,
            'country': "Brazil",
            'author': "Giovanni Silva de Oliveira"
        },
        {
            'id': "B",
            'flavor': "sklearn",
            'r2': .7,
            'mae': 2000,
            'mape': .18,
            'rmse': .2004,
            'algorithm': "Gradient Boosting",
            'data_year': 2025,
            'country': "Brazil",
            'author': "Edson Arantes do Nascimento"
        },
        {
            'id': "C",
            'flavor': "sklearn",
            'r2': .8,
            'mae': 1987,
            'mape': .09,
            'rmse': .2025,
            'algorithm': "Regression",
            'data_year': 2015,
            'country': "France",
            'author': "Neymar Jr"
        }
    ]
    city_records = [
        {
            'city': 'São José dos Campos',
            'models_id': 'A',
            'country': 'Brazil'
        },
        {
            'city': 'São Paulo',
            'models_id': 'A',
            'country': 'Brazil'
        },
        {
            'city': 'São José dos Campos',
            'models_id': 'B',
            'country': 'Brazil'
        },
        {
            'city': 'Belo Horizonte',
            'models_id': 'B',
            'country': 'Brazil'
        },
        {
            'city': 'Dijon',
            'models_id': 'C',
            'country': 'France'
        },
        {
            'city': 'Paris',
            'models_id': 'C',
            'country': 'France'
        }
    ]
    inputs_records = [{
        'models_id': 'A',
        'column_name': 'n_bedrooms',
        'label': 'Bedrooms',
        'type': 'int',
        'options': '',
        'description': 'Number of bedrooms.',
        'unit': '',
    }]

    with TemporaryDirectory() as tmpdir:
        database_path = f"{tmpdir}/database.db"
        database = Database(database_path)
        database.initialize_schema()

        for record in model_records:
            database.insert_data('models', record)
        for record in city_records:
            database.insert_data('cities', record)
        for record in inputs_records:
            database.insert_data('inputs', record)

        yield database


def test_country(get_test_db):
    database = get_test_db
    df = pd.read_sql_query(country, database.con)
    assert df['country'].to_list() == ['Brazil', 'France']


def test_cities(get_test_db):
    database = get_test_db
    df = pd.read_sql_query(cities, database.con, params={'country': 'Brazil'})
    assert df['city'].to_list() == [
    'Belo Horizonte', 'São José dos Campos', 'São Paulo']

    df = pd.read_sql_query(cities, database.con, params={'country': 'France'})
    assert df['city'].to_list() == [
    'Dijon', 'Paris']


def test_models_of_city(get_test_db):
    database = get_test_db

    # test sort by data_year
    query = models_of_city.format(sort='data_year DESC')
    df = pd.read_sql_query(
            query,
            database.con,
            params={'city':'São José dos Campos'}
        )
    assert df.loc[0, 'data_year'] == 2025

    # test sort by mape
    query = models_of_city.format(sort='mape')
    df = pd.read_sql_query(
            query,
            database.con,
            params={'city':'São José dos Campos'}
        )
    assert df.loc[0, 'mape'] == .18