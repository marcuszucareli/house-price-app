import pandas as pd
import os
from fastapi import FastAPI, HTTPException, Query
from database.queries import queries
from database.crud import *
from api.schemas import *


with open(file='./api/description.md') as f:
    description = f.read()
    description = description.format(
        API_BASE_URL = os.getenv("API_BASE_URL")
    )

app = FastAPI(
    title="Real Estate Estimator API",
    description=description,
    version="1.0.0",
    contact={
        "Github": "https://github.com/marcuszucareli/house-price-app"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)


@app.get(
    "/",
    summary="Check API status",
    description="Returns the current status of the API.",
    # response_description="App is up and running.",
    response_model= StatusResponse,
    tags=["Health"]
)
def status():
    return {"status": "running"}


@app.get(
    "/countries/",
    summary="Get Countries",
    description="Returns a list of countries with available models.",
    response_model= GetCountriesResponse,
    tags=["Consulting"]
)
def get_countries():
    """
    Get a list of countries with models.

    Returns:
    countries list[str]: List of countries with models.
    """
    query = queries['get_all_countries'] 
    df = execute_with_pandas(query)
    countries = df['country'].to_list()
    return {"countries": countries}


@app.get("/cities/",
    tags=["Consulting"],
    response_model=GetCitiesResponse
)
def get_cities(
    country: str = Query(
        default='all',
        title='country',
        description="Optional parameter to filter cities by country. The " \
        "parameter must be named " \
        "according to [ISO 3166 standards](https://www.iso.org/" \
        "iso-3166-country-codes.html).",
        openapi_examples={
            "all": {
                "value": "all",
                "summary": "All",
                "description": "Getting all cities",
            },
            "example2": {
                "value": "Brazil",
                "summary": "Brazil",
                "description": "Filtering brazilian cities ",
            }
        }
    )
):

    if country == 'all':
        param = {'country': None}
    else:
        param = {'country': country}

    query = queries['get_all_cities'] 
    df = execute_with_pandas(query, param)
    countries = df['city'].to_list()
    return {"cities": countries}


@app.get(
    '/models/',
    tags=["Consulting"],
    response_model=GetModelsResponse
)
def get_models(
    city: str = Query(
        default='all',
        title='city',
        description="Filter models by city.",
        openapi_examples={
            "all": {
                "value": "all",
                "summary": "",
                "description": "Getting all models",
            },
            "city": {
                "value": "Belo Horizonte",
                "summary": "",
                "description": "Filtering by city",
            }
        }
    ),
    sortBy: GetModelsCategory = Query(
        default='year',
        title='Sorting options',
        description=(
            "Sort models by date of the model or its metrics. Available" \
            " options are:\n\n"
            "- **year**: The year when the data to train the model was collected.\n"
            "- **mae**: Mean absolute error.\n"
            "- **mape**: Mean absolute percentage error.\n"
            "- **r2**: R-squared.\n"
            "- **rmse**: Root mean squared error."
        ),
        openapi_examples={
            "year": {
                "value": "year",
                "description": "Sort by year",
            },
            "mape": {
                "value": "mape",
                "description": "Sort by mean absolute percentage error.",
            }
        }
    )
):

    query = queries['get_models_from_city']
    
    match sortBy:
        case 'year':
            formatted_query = \
                query.format(sort_by='data_year DESC')
        case 'mae':
            formatted_query = \
                query.format(sort_by='mae')
        case 'mape':
            formatted_query = \
                query.format(sort_by='mape')
        case 'r2':
            formatted_query = \
                query.format(sort_by='r2 DESC')
        case 'rmse':
            formatted_query = \
                query.format(sort_by='rmse')
        case _:
            raise HTTPException(
                status_code=400, detail="Invalid sortBy parameter")
    
    if city == 'all':
        param = {'city': None}
    else:
        param = {'city': city}
        
    df = execute_with_pandas(formatted_query, param)
    cities = df.to_dict(orient="records")

    return {"models": cities}


@app.get(
    '/inputs/',
    tags=['Consulting'],
    # response_model='alterar' 
)
def get_inputs(model_id: str = 
    Query(
        title='Model id',
        description=(
            "Get the required inputs to use the model" \
        ),
        openapi_examples={
            "model id": {
                "value": "A",
                "description": "The id of the desired model."
            }
        }
    )
):
    query = queries['get_inputs']
    param = {'model_id': model_id}
    df = execute_with_pandas(query, param)
    inputs = df.to_dict(orient="records")

    return {'inputs': inputs}