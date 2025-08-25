from tests.conftest import std_model_cases, standard_uuid
import os

def test_status(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'running'}


def test_get_countries(client):
    countries_list = [model['cities'][0]['country'] for model in std_model_cases]
    countries_list = list(set(countries_list))
    countries_list = sorted(countries_list)
    response = client.get('countries')
    assert response.json() == {'countries': countries_list}


def test_get_cities(client):
    all_cities = {}
    br_cities = {}

    for model in std_model_cases:
        for city in model['cities']:
            city_name = city['name'] + ' (' + city['hierarchy'] + ')'
            all_cities[city_name] = city['wikidata_id']
            if city['country'] == 'Brazil':
                br_cities[city_name] = city['wikidata_id']
    all = client.get('cities', params={'country': 'all'})
    all_implicit = client.get('cities')
    brazil = client.get('cities', params={'country': 'Brazil'})

    assert all.json() == all_implicit.json() == {'cities': all_cities}
    assert brazil.json() == {'cities': br_cities}


def test_get_models(client):
    
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


def test_get_model(client):
    model = client.get(f'model/{standard_uuid}')
    model = model.json()
    assert model['model']['id'] == str(standard_uuid)


def test_get_inputs(client):
    model = std_model_cases[-1]

    expected_inputs = [input_['column_name'] for input_ in model['inputs']]

    inputs = client.get(f'inputs/{standard_uuid}')
    inputs = inputs.json()
    inputs = inputs['inputs']

    assert len(inputs) > 0

    for input_ in inputs:
        assert input_['models_id'] == str(standard_uuid)
        assert input_['column_name'] in expected_inputs


def test_predict(client):
    features = {
        'features': {
            "rooms": 3,
            "parking": 2,
            "bathrooms": 1,
            "area": 90,
            "has_multiple_parking_spaces": True,
            "neighbourhood": "Jardim Esplanada",
            "lat_value": -23.1789,
            "lon_value": -45.8869,
        }
    }

    inputs = client.get(f'/inputs/{standard_uuid}')
    inputs = inputs.json()

    prediction = client.post(f'/predict/{standard_uuid}', json=features)
    prediction = prediction.json()
    
    assert isinstance(prediction['predict']['mape'], float)
    assert isinstance(prediction['predict']['property_price'], float)
