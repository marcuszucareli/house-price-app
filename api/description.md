
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.95-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

# About
Welcome to the Real Estate Estimator API. This API is part of a [larger 
project](https://github.com/marcuszucareli/house-price-app) that includes a web 
application and is maintained by our contributors under an open source model.

Here you can estimate properties prices using Machine Learning Models from 
different cities around the world.

# Features
- Query models by metrics, countries or cities
- Estimate the price of a property

# Getting started
In order to estimate the price of a property, you will need the ID of the 
model you want to use. Models are ultimately linked to cities, which is why we 
encourage you to use the city to search for the appropriate model.

## Finding a model
Let's see the models for the welcoming city of Belo Horizonte in Brazil

```python
import requests

# Request URL
url = "{API_BASE_URL}/models/"

# Params
params = {{{{
    "city": "Belo Horizonte",
    "sortBy": "year" # You can also sort by the metrics mae, mape, r2 and rmse
}}}}

# Call the API
response = requests.get(url, params=params)

# Get the json data
data = response.json()
```

## Estimating the value
As you can see in the json bellow, there are two models for the city, let's use
B, since it is the most recent one.
```json
{{
  "models": [
    {{
      "id": "B",
      "flavor": "xgboosting",
      "data_year": 2025,
      "mae": 2000,
      "mape": 0.18,
      "r2": 0.7,
      "rmse": 0.2004,
      "algorithm": "xgboosting",
      "country": "Brazil",
      "author": "Edson Arantes do Nascimento"
    }},
    {{
      "id": "A",
      "flavor": "sklearn",
      "data_year": 2011,
      "mae": 1963,
      "mape": 0.2002,
      "r2": 0.1962,
      "rmse": 0.2004,
      "algorithm": "Random forest",
      "country": "Brazil",
      "author": "Giovanni Silva de Oliveira"
    }}
  ]
}}
```

More information can be found in the [Docs](/redoc#tag/Health) section. You can also or you can also [Try it here](/docs).
