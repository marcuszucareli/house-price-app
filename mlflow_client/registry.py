"""
Regsitry.py

This module contains functions to be used as connection between the streamlit
app and the Mlflow client.

Author: Marcus Zucareli
Date: 2025-05-29
"""

import json
from mlflow_client.factory import get_mlflow_client

class Models():
    def __init__(self):
        self.client = get_mlflow_client()
        self.models = self.client.get_models()
    

    def get_places(self) -> dict[str, list[str]]:
        """
        Get all cities with available models, grouped by country.

        Returns:
            dict[str, list[str]]: A dict where the keys are country names and
            values are lists that have available models.
        """

        places = {}
        
        for model in self.models:
            country = model.tags['country']
            if country not in places.keys():
                places[country] = []
            
            cities_list = json.loads(model.tags['cities'])
            for city in cities_list:
                if city not in places[country]:
                    places[country].append(city)
            
            places[country].sort()
        
        places = dict(sorted(places.items()))
        return places


    def get_inputs(self, city: str) -> dict[str, dict]:
        """
        Get the inputs needed to model prediction.

        Args:
            city (str): The name of the city to get the inputs from.
        Returns:
            dict[str, dict]: A dict containing the frontend name, type and 
            options (for categorical variables) of each input.
        """

        # Get corresponding model
        for model in self.models:
            cities = json.loads(model.tags['cities'])
            if city in cities:
                return json.loads(model.tags['inputs'])

        raise KeyError('City not found')