from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StatusResponse(BaseModel):
    status: str = Field(
        default_factory='running',
        description="Returns 'running' if API is up."
    )

    model_config={
        'json_schema_extra': {
            "examples": [{
                "status": "running"
            }]
        }
    }


class GetCountriesResponse(BaseModel):
    countries: list[str] = Field(
        default_factory=list,
        description="List of countries supported by available models, named " \
        "according to [ISO 3166 standards](https://www.iso.org/" \
        "iso-3166-country-codes.html)."
    )

    model_config={
        'json_schema_extra': {
            "examples": [{
                "countries": ['Brazil', 'France']
            }]
        }
    }


class GetCitiesResponse(BaseModel):
    cities: list[str] = Field(
        default_factory=list,
        description="List of cities supported by available models sorted " \
        "alphabetically."
    )

    model_config={
        'json_schema_extra': {
            "examples": [{
                "cities": ['Dijon', 'Paris']
            }]
        }
    }


class GetModelsCategory(str, Enum):
    year = 'year'
    mae = 'mae'
    mape = 'mape'
    r2 = 'r2'
    rmse = 'rmse'


class ModelItem(BaseModel):
    id: str = Field(description='The id of the model.', examples=['A'])
    flavor: str = Field(description='The library used to create the model.',
                         examples=['sklearn'])
    data_year: int = Field(
        description='The year when the data to train the model was collected.',
        examples=[2025])
    mae: float = Field(description='Mean absolute error.', examples=[50_000.3])
    mape: float = Field(description='Mean absolute percentage error.',
                        examples=[.80])
    r2: float = Field(description='R-squared', examples=[.83])
    rmse: float = Field(description='Root mean squared error.',
                        examples=[98_000.05])
    algorithm: str = Field(description='Type of algorithm used by the model ' \
    '(e.g. Random Forest, Regression)', examples=['Random Forest'])
    author: str = Field(description='The name of the author of the model.',
                        examples=['Edson Arantes do Nascimento'])
    links: str = Field(
        description='Links provided by the author.',
        examples=["{'linkedin': 'www.linkedin.com'}"])


class GetModelsResponse(BaseModel):
    models: list[ModelItem] = Field(
        default_factory=list,
        description=(
            "List of available models in the chosen city and sorted by the "
            "chosen parameter.\n\n"
            "- **id**: The id of the model.\n"
            "- **flavor**: The library used to create the model.\n"
            "- **data_year**: The year when the data to train the model was" 
            " collected.\n"
            "- **mae**: Mean absolute error.\n"
            "- **mape**: Mean absolute percentage error.\n"
            "- **r2**: R-squared.\n"
            "- **rmse**: Root mean squared error.\n"
            "- **algorithm**: Type of algorithm used by the model (e.g. "
            "Random Forest, Regression)\n"
            "**country**: The country where the model is located\n"
            "**author**: The name of the author of the model.\n"
            "**links**: Relevant links provided by the author.\n"
        )
    )
    