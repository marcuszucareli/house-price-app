import json
from mlflow_client.factory import get_mlflow_client

def get_places():
    client = get_mlflow_client()
    models = client.get_models()

    places = {}
    
    for model in models:
        country = model.tags['country']
        if country not in places.keys():
            places[country] = []
        
        cities_list = json.loads(model.tags['city'])
        for city in cities_list:
            if city not in places[country]:
                places[country].append(city)
        
        places[country].sort()
    
    places = dict(sorted(places.items()))
    return places

