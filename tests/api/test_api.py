import pytest
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

def test_status():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'running'}


def test_get_countries():
    response = client.get('countries')
    assert response.json() == {'countries': ['Brazil', 'France']}


def test_get_cities():
    all_cities = ['Belo Horizonte', 'Dijon', 'Jacareí', 'Paris',
                   'São José dos Campos', 'Taubaté']
    br_cities = ['Belo Horizonte', 'Jacareí', 'São José dos Campos', 'Taubaté']
    fr_cities = ['Dijon', 'Paris']

    all = client.get('cities', params={'country': 'all'})
    all_implicit = client.get('cities')
    brazil = client.get('cities', params={'country': 'Brazil'})
    france = client.get('cities', params={'country': 'France'})

    assert all.json() == all_implicit.json() == {'cities': all_cities}
    assert brazil.json() == {'cities': br_cities}
    assert france.json() == {'cities': fr_cities}


def test_get_models():
    models = {
        'models': [
            {
                'id': 'A',
                'flavor': 'sklearn',
                'data_year': 2011, 
                'mae': 1963.0, 
                'mape': 0.2002, 
                'r2': 0.1962, 
                'rmse': 0.2004, 
                'algorithm': 'Random forest',
                'author': 'Giovanni Silva de Oliveira',
                'links': '{"linkedin": "www.linkedin.com", ' \
                    '"github": "www.github.com"}'
            },
            {
                'id': 'B',
                'flavor': 'xgboosting', 
                'data_year': 2025, 
                'mae': 2000.0, 
                'mape': 0.18, 
                'r2': 0.7, 
                'rmse': 0.2004, 
                'algorithm': 'xgboosting', 
                'author': 'Edson Arantes do Nascimento',
                'links': '{"linkedin": "www.linkedin.com", ' \
                    '"github": "www.github.com"}'
            }, 
            {
                'id': 'C', 
                'flavor': 'sklearn', 
                'data_year': 2015, 
                'mae': 1987.0, 
                'mape': 0.09, 
                'r2': 0.8, 
                'rmse': 0.2025, 
                'algorithm': 'Regression', 
                'author': 'Neymar Jr', 
                'links': '{"linkedin": "www.linkedin.com", '\
                    '"github": "www.github.com"}'
            }
        ]
    }
    
    all = client.get('models', params={'city': 'all'})
    all_implicit = client.get('models')
    belo_horizonte =  client.get('models', params={'city': 'Belo Horizonte'})
    taubate =  client.get('models', params={'city': 'Taubaté'})
    dijon =  client.get('models', params={'city': 'Dijon'})
    santos =  client.get('models', params={'city': 'Santos'})
    belo_horizonte_by_mape =  client.get('models',
        params={'city': 'Belo Horizonte', 'sortBy':'mape'})
    assert all.json() == all_implicit.json()
    assert belo_horizonte.json() == {
        'models': [models['models'][1], models['models'][0]]}
    assert taubate.json() == {'models': [models['models'][0]]}
    assert dijon.json() == {'models': [models['models'][2]]}
    assert santos.json() == {'models': []}
    assert belo_horizonte_by_mape.json() == {
        'models': [models['models'][1], models['models'][0]]}
    