import pandas as pd
import os
import mlflow
import json
from fastapi import FastAPI, HTTPException, Query, Path
from database.queries import queries
from database.crud import *
from api.schemas import *
from functools import lru_cache
from tests.conftest import standard_uuid

# Get storage path
STORAGE_PATH = os.getenv('STORAGE_PATH')
MODEL_FOLDER_NAME = os.getenv('MODEL_FOLDER_NAME')

# Cache mlflow models
@lru_cache(maxsize=2)
def get_model_cached(model_path: str):
    print(model_path)
    try:
        return mlflow.pyfunc.load_model(model_path)
    except Exception:
        raise RuntimeError(f"Error loading model")


# API description
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
    df["city"] = df['city'] + ' (' + df['hierarchy'] + ')'
    cities_dict = dict(zip(df["city"], df["id"]))
    return {"cities": cities_dict}


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
        param = {'city_id': None}
    else:
        param = {'city_id': city}
        
    df = execute_with_pandas(formatted_query, param)
    df['links'] = df['links'].apply(lambda x: json.loads(x))
    cities = df.to_dict(orient="records")
    class_models = []

    for model in cities:
        class_models.append(ModelItem(**model))

    return GetModelsResponse(models=class_models)


@app.get(
    "/model/{model_id}",
    response_model=GetModelResponse
)
def get_model(model_id: str = Path(
        title='Model id',
        description=(
            "Get model's metadata."
        ),
        openapi_examples={
            "model id": {
                "value": f"{standard_uuid}",
                "description": "The id of the desired model."
            }
        }
    )):
    
    query = queries['get_model']
    df = execute_with_pandas(query, {'model_id': model_id})
    df['links'] = df['links'].apply(lambda x: json.loads(x))
    model = df.to_dict(orient="records")
    if model:
        return GetModelResponse(model=ModelItem(**model[0]))
    else:
        raise HTTPException(
            status_code=404,
            detail="Model not found")


@app.get(
    '/inputs/{model_id}',
    tags=['Consulting'],
    response_model=GetInputsResponse
)
def get_inputs(model_id: str = 
    Path(
        title='Model id',
        description=(
            "Get the required inputs to use the model."
        ),
        openapi_examples={
            "model id": {
                "value": f"{standard_uuid}",
                "description": "The id of the desired model."
            }
        }
    )
):
    
    query = queries['get_inputs']
    param = {'model_id': model_id}

    df = execute_with_pandas(query, param)
    df.drop('id', axis=1, inplace=True)
    df['options'] = df['options'].apply(lambda x: json.loads(x))
    
    inputs = df.to_dict(orient="records")
    class_inputs = []
    for input in inputs:
        class_inputs.append(InputItem(**input))
    
    return GetInputsResponse(inputs=class_inputs)


@app.post(
    "/predict/{model_id}",
    tags=['Predicting'],
    # response_model=GetInputsResponse
)
def predict(
    features: PredictRequest,
    model_id: str = 
    Path(
        title='Model id',
        description=(
            "Predict the property value using the model of provided id."
        ),
        openapi_examples={
            "model id": {
                "value": f"{standard_uuid}",
                "description": "The id of the desired model."
            }
        }
    ),
    ):

    print(features)
    print(model_id)
    print('-'*70)

    # Get model's inputs
    inputs = get_inputs(model_id)
    
    # Validate inputs
    try:
        validate_input_data(inputs.inputs, features.features)
    except Exception as e:
        raise HTTPException(
            status_code = 422,
            detail = str(e)  
        )
    
    # Get model
    try:
        model = get_model_cached(
            f"{STORAGE_PATH}/{model_id}/{MODEL_FOLDER_NAME}")
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
    
    try:
        df = pd.DataFrame([features.features])
        property_price = model.predict(df)
        prediction = {
            'mape': get_model(model_id).model.mape,
            'property_price': round(float(property_price), 2)
        }

        return PredictResponse(predict=prediction)
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Error predicting the price: {str(e)}"
        )