import pytest
import uuid
import textwrap
import json

standard_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")

# Tables columns
models_table_columns = [
    'id',
    'flavor',
    'r2',
    'mae',
    'mape',
    'rmse',
    'algorithm',
    'data_year',
    'author',
    'links'
]

cities_table_columns = [
    'id',
    'city',
    'models_id',
    'country'
]

inputs_table_columns = [
    'id',
    'models_id',
    'column_name',
    'lat',
    'lng',
    'label',
    'type',
    'options',
    'description',
    'unit'
]

# Standard inputs and models
std_input_cases = [
    # Type categorical
    {
        'column_name': "neighbourhood",
        'lat': "lat",
        'lng': "lng",
        'label': "Neighbourhood",
        'type': "categorical",
        'options': ['Morumbi', 'América'],
        'description': 'Property neighbourhood',
        'unit': None
    },
    # Type bool
    {
        'column_name': "is_new",
        'lat': "lat",
        'lng': "lng",
        'label': "Is your house new?",
        'type': "bool",
        'options': [],
        'description': 'If your house has less than 5 years',
        'unit': None
    },
    # Type int
    {
        'column_name': "n_bedrooms",
        'lat': "lat",
        'lng': "lng",
        'label': "Number of bedrooms in the house",
        'type': "int",
        'options': [],
        'description': '',
        'unit': 'un'
    },
    # Type float
    {
        'column_name': "area_m2",
        'lat': "lat",
        'lng': "lng",
        'label': "Area",
        'type': "float",
        'options': [],
        'description': 'The property size in m².',
        'unit': 'm²'
    },
    # Type maps
    {
        'column_name': 'map',
        'lat': 'latitude',
        'lng': 'longitude',
        'label': "Coordinates",
        'type': "map",
        'options': [],
        'description': "house's Latitude and Longiude",
        'unit': None
    }
]

std_model_cases = [
    {
        'id': str(standard_uuid),
        'model_link': 'https://www.santosfc.com.br/',
        'flavor': 'sklearn',
        'author': 'Edson Arantes do Nascimento',
        'algorithm': 'regression',
        'data_year': 1999,
        'country': 'Brazil',
        'cities': ["Belo Horizonte", "Três Corações"],
        'inputs': std_input_cases,
        'links': {
            "Github": "https://github.com/",
            "Linkedin": "https://www.linkedin.com/"
        }
    },
    {
        'id': str(standard_uuid).replace('0','1'),
        'model_link': 'https://en.wikipedia.org/wiki/Douglas_Adams',
        'flavor': 'sklearn',
        'author': 'Douglas Adams',
        'algorithm': 'gradient boosting',
        'data_year': 1998,
        'country': 'England',
        'cities': ["Cambridge"],
        'inputs': std_input_cases[1:],
        'links': {
            "Github": "https://github.com/",
        }
    },
    {   
        'id': str(standard_uuid).replace('0','2'),
        'model_link': 'https://www.aurora-music.com/',
        'flavor': 'sklearn',
        'author': 'Aurora Aksnes',
        'algorithm': 'random forest',
        'data_year': 1997,
        'country': 'Norway',
        'cities': ["Oslo", "Bergen"],
        'inputs': std_input_cases[1:-1],
        'links': {
            "Linkedin": "https://www.linkedin.com/"
        }
    },
]


# Write/update dev_db 
def write_sql_file():

    queries = []

    metric_values = 99
    # models
    for model in std_model_cases:
        
        models_query = textwrap.dedent(f"""\
        INSERT INTO models VALUES (
        '{model['id']}',
        '{model['flavor']}',
        {str(metric_values / 100)},
        {str(metric_values)},
        {str(metric_values / 100)},
        {str(metric_values / 100)},
        '{model['algorithm']}',
        {model['data_year']},
        '{model['author']}',
        '{json.dumps(model['links'])}'
        );
        """)

        queries.append(models_query)

        for city in model['cities']:
            city_query = textwrap.dedent(f"""\
            INSERT INTO cities VALUES (
            NULL,
            '{city}',
            '{model['id']}',
            '{model['country']}'
            );
            """)

            queries.append(city_query)
        
        for input in model['inputs']:
            input_query = textwrap.dedent(f"""\
            INSERT INTO inputs VALUES (
            NULL,
            '{model['id']}',
            '{input['column_name']}',
            '{input['lat']}',
            '{input['lng']}',
            '{input['label']}',
            '{input['type']}',
            '{json.dumps(input['options'], ensure_ascii=False)}',
            {f'"{input['description']}"' if input['description'] != '' else 'NULL'},
            {f"'{input['unit']}'" if input['unit'] is not None else 'NULL'}
            );
            """)

            queries.append(input_query)

        metric_values -= 1
    
    with open('database/dev_db.sql', 'w') as f:
        for query in queries:
            f.write(query)

write_sql_file()
@pytest.fixture()
def temp_db_path(monkeypatch, tmp_path):
    DB_PATH = f'{str(tmp_path)}/db_test.db'
    monkeypatch.setenv('DB_PATH', DB_PATH)
    
    from database.init_db import init_db

    init_db()

    yield DB_PATH


@pytest.fixture()
def empty_temp_db_path(monkeypatch, tmp_path):
    DB_PATH = f'{str(tmp_path)}/db_test.db'
    monkeypatch.setenv('DB_PATH', DB_PATH)
    
    from database.connection import get_connection

    with open("database/schemas.sql") as f:
        schema = f.read()

        with get_connection() as conn:
            c = conn.cursor()
            c.executescript(schema)

    yield DB_PATH