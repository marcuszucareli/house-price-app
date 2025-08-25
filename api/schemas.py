from pydantic import BaseModel, Field
from typing import Optional, Any, Union
from enum import Enum


class StatusResponse(BaseModel):
    status: str = Field(
        default_factory='running',
        description="Returns status 'running' if API is up."
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
                "countries": ['Brazil', 'England']
            }]
        }
    }


class GetCitiesResponse(BaseModel):
    cities: dict[str, str] = Field(
        default_factory=dict,
        description="List of cities supported by available models sorted " \
        "alphabetically."
    )

    model_config={
        'json_schema_extra': {
            "examples": [{
                "cities": ['Belo Horizonte', 'Bergen']
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
    id: str = Field(description="Model's id.", examples=['A'])
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
    links: dict = Field(
        description='Links provided by the author.',
        examples=[{'linkedin': 'www.linkedin.com'}])


class GetModelsResponse(BaseModel):
    models: list[ModelItem] = Field(
        default_factory=list,
        description=(
            "List of available models in the chosen city sorted by the "
            "chosen parameter."
        )
    )


class GetModelResponse(BaseModel):
    model: ModelItem


class InputItem(BaseModel):
    models_id: str = Field(
        description="Model's id.",
        example='00000000-0000-0000-0000-000000000000')
    column_name: str = Field(
        description='Name of the column input in the model. Use an empty ' \
        'string when input type is "map".',
        example='area_m²'
    )
    lat: Union[str, None] = Field(
        description="Name of the latitude column in the machine learning " \
        "model. Used only when input type is 'map'.",
        example='lat'
    )
    lng: Union[str, None] = Field(
        description="Name of the longitude column in the machine learning " \
        "model. Used only when input type is 'map'.",
        example='lng'
    )
    label: str = Field(
        description="Label used in the web app.", example='Area')
    type: str = Field(
        description="The type of input. Options are: int, float, bool," \
        " categorical, map."
        ,
        example='int'
    )
    options: list[str] = Field(
        default_factory=list,
        description="List of options when the input type is 'categorical'.",
        example=['Block 1', 'Block 2', 'Block 3']
    )
    description: Optional[str] = Field(
        None,
        description='The description of the field used in the web app',
        example='The neighbourhood of the property.'
    )
    unit: Optional[str] = Field(
        None,
        description='The unit of the input',
        example='m²'
    )
    

class GetInputsResponse(BaseModel):
    inputs: list[InputItem] = Field(
        title="Inputs",
        default_factory=list,
        description="""
List of inputs of the model. There're 5 type of inputs, each one of them 
expects different data types when predicting:
- **int**, **float**, and **bool** are expected to receive values of 
the corresponding data type.
- **categorical** inputs expect a string value that must match one of the 
entries defined in the options field of the same input.
- **map** inputs expect latitude and longitude values to be provided as float
 numbers, using the field names specified in the lat and lng attributes of
the input definition."


"""
    )


class PredictRequest(BaseModel):
    features: dict[str, Any]


class PredictResponse(BaseModel):
    predict: dict[str, float]


def validate_input_data(
        inputs: list[InputItem],
        features: dict[str, Any]) -> dict[str, Any]:
    
    required_fields = set()

    for input_def in inputs:
        input_type = input_def.type

        if input_type == "map":
            required_fields.update([input_def.lat, input_def.lng])

            # Check if lat/lng fields are present and are floats
            for field in [input_def.lat, input_def.lng]:
                if field not in features:
                    raise ValueError(
                        f"Missing required field: '{field}' (from map input)")
                if not isinstance(features[field], (float, int)):
                    raise TypeError(
                        f"Field '{field}' must be a float (lat/lng).")
        else:
            field = input_def.column_name
            required_fields.add(field)

            if field not in features:
                raise ValueError(f"Missing required field: '{field}'.")

            value = features[field]

            # type validation
            if input_type == "int":
                if not isinstance(value, int):
                    raise TypeError(f"Field '{field}' must be of type int.")
            elif input_type == "float":
                if not isinstance(value, (float, int)):
                    raise TypeError(f"Field '{field}' must be of type float.")
            elif input_type == "bool":
                if not isinstance(value, bool):
                    raise TypeError(f"Field '{field}' must be of type bool.")
            elif input_type == "categorical":
                if not isinstance(value, str):
                    raise TypeError(
                        f"Field '{field}' must be a string (categorical).")
                if value not in input_def.options:
                    raise ValueError(
                        f"Value '{value}' for field '{field}' is not a " \
                        f"valid option: {input_def.options}")
            elif input_type == "str":
                if not isinstance(value, str):
                    raise TypeError(f"Field '{field}' must be of type str.")

    extra_fields = set(features.keys()) - required_fields
    if extra_fields:
        raise ValueError(
        f"Unexpected fields in input data: {sorted(extra_fields)}. "
        f"Only the following fields are allowed: {sorted(required_fields)}."
    )