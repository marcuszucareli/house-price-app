"""
Regsitry.py

This module contains functions to be used as connection between the streamlit
app and the Mlflow client.

Author: Marcus Zucareli
Date: 2025-05-29
"""

import json
from mlflow_client.factory import get_mlflow_client

def get_places() -> dict[str, list[str]]:
    """
    Get all cities with available models, grouped by country.

    Returns:
        dict[str, list[str]]: A dict where the keys are country names and
        values are lists that have available models.
    """
    client = get_mlflow_client()
    models = client.get_models()

    places = {}
    
    for model in models:
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

