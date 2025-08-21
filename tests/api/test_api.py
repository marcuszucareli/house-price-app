from fastapi.testclient import TestClient
from api.api import app
from tests.conftest import std_model_cases

client = TestClient(app)

def test_status(temp_db_path):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'running'}


def test_get_countries(temp_db_path):
    countries_list = [model['country'] for model in std_model_cases]
    print(countries_list)
    countries_list = sorted(countries_list)
    response = client.get('countries')
    assert response.json() == {'countries': countries_list}


def test_get_cities(temp_db_path):
    all_cities = [
        city
        for item in std_model_cases
        for city in item['cities']
    ]
    br_cities = next(
        (
            modelo['cities'] 
            for modelo in std_model_cases 
            if modelo['country'] == 'Brazil'
        ),
        None
    )
    all = client.get('cities', params={'country': 'all'})
    all_implicit = client.get('cities')
    brazil = client.get('cities', params={'country': 'Brazil'})

    assert all.json() == all_implicit.json() == {'cities': sorted(all_cities)}
    assert brazil.json() == {'cities': sorted(br_cities)}


def test_get_models(temp_db_path):
    
    all = client.get('models', params={'city': 'all'})
    all_implicit = client.get('models')

    assert all.json() == all_implicit.json()
    assert len(all.json()['models']) == \
        len(all_implicit.json()['models']) == \
        len(all_implicit.json()['models'])

    all_cities = [
        city
        for item in std_model_cases
        for city in item['cities']
    ]

    for city in all_cities:
        res = client.get('models',
            params={'city': city, 'sortBy':'mape'})
        res = res.json()
        res = res['models']

        for api_model in res:
            for std_model in std_model_cases:
                if api_model['id'] == std_model['id']:
                    assert city in std_model['cities']
                else:
                    assert city not in std_model['cities']


