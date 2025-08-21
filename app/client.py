import requests
import json
import os
import logging

API_BASE_URL = os.getenv('API_BASE_URL')

class Models:

    def call_api(self, endpoint, params=None, path='', body=None):
        try:
            url = f'{API_BASE_URL}/{endpoint}/{path}'
            if body is not None:
                response = requests.post(url, params=params, json=body)
            else:
                response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data[endpoint]
            else:
                logging.error(response)
                return None
        except Exception as e:
            logging.error(f'endpoint: {endpoint}')
            logging.error(f'params: {params}')
            logging.error(f'path: {path}')
            logging.error(f'body: {body}')
            logging.error(e)
            return None
        
    def __init__(self):
        self.countries = self.call_api('countries')
        self.health_check = True if self.countries != None else False
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
        response = self.call_api('inputs', path=f'{self.model['id']}')
        self.inputs = response

    def get_prediction(self, body):
        response = self.call_api(
            'predict', path=f'{self.model['id']}', body=body)
        return response

    def reset(self, level=0):
        for key, value in self._index.items():
            if value > level:
                setattr(self, key, None)
    
    def printall(self):
        for key in self._index.keys():
            print(key, getattr(self, key))
        print('-'*50)
