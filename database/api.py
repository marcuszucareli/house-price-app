import pandas as pd
from fastapi import FastAPI, HTTPException
from database.queries import queries
from database.crud import *

app = FastAPI()


@app.get("/")
def is_running():
    return {"is_running": "True"}


@app.get("/countries/")
def get_countries():
    query = queries['get_all_countries'] 
    df = execute_with_pandas(query)
    countries = df['country'].to_list()
    return {"countries": countries}


@app.get("/cities/")
def get_countries(country: str):

    if country == 'all':
        param = {'country': None}
    else:
        param = {'country': country}

    query = queries['get_all_cities'] 
    df = execute_with_pandas(query, param)
    print(df)
    countries = df['city'].to_list()
    return {"cities": countries}


@app.get('/models/')
def get_models(city: str, sortBy: str ='year'):

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
    df.set_index("id").to_dict(orient="index")
    cities = df.set_index("id").to_dict(orient="index")

    return {"models": cities}

