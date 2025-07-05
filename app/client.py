import requests
import json
import os

API_BASE_URL = os.getenv('API_BASE_URL')

class Models:

    def call_api(self, endpoint, params=None):
        url = f'{API_BASE_URL}/{endpoint}'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data[endpoint]
        else:
            return None

    def __init__(self):
        self.countries = self.call_api('countries')
        self.country = None
        self.cities = None
        self.city = None
        self.model = None
        self.inputs = None
        self._index = {
            "countries": 1,
            "country": 2,
            "cities": 3,
            "city": 4,
            "model": 5,
            "inputs": 6
        }
    
    def get_cities(self):
        self.cities = self.call_api('cities', {'country': self.country})
    
    def get_model(self):
        models = self.call_api('models', {'city': self.city})
        if models:
            self.model = models[0]

    def get_inputs(self):
        response = self.call_api('inputs', {'model_id': self.model['id']})
        for i, item in enumerate(response):
            if item['type'] == 'categorical':
                response[i]['options'] =  json.loads(response[i]['options'])
        self.inputs = response

    def reset(self, level=0):
        for key, value in self._index.items():
            if value > level:
                setattr(self, key, None)
    
    def printall(self):
        for key in self._index.keys():
            print(key, getattr(self, key))
        print('-'*50)
