import pytest
import pandas as pd
import numpy as np
import pathlib
from datetime import datetime
from mlflow_client.model_logging import Inputs, Cities, \
    ModelLogInput, max_chars
from tests.mlflow_client.conftest import std_input_cases, std_model_cases, \
    base_ModelLogInput


@pytest.mark.parametrize("input_data", std_input_cases)
def test_Inputs_validation_success(input_data):
    model_input = Inputs(**input_data)
    assert isinstance(model_input, Inputs)


@pytest.mark.parametrize(
    "input_data, expected",
    [   
        # column_name string size
        ({'column_name': "a"*(max_chars+1)}, ValueError),
        # label string size
        ({'label': "a"*(max_chars+1)}, ValueError),
        # Type not listed
        ({'type': "a"}, ValueError),
        # Only one option
        ({'options': ['Morumbi'], 'type': 'category'}, ValueError),
        # Description string size
        ({'description': "a"*250}, ValueError),
        # Unit string size
        ({'unit': "a"*(max_chars+1)}, ValueError),
        # Map type and lat is None
        ({'type':"map", 'lat': None}, ValueError),
        # Map type and lng is None
        ({'type':"map", 'lng': None}, ValueError)
    ]
)
def test_Inputs_validation_error(input_data, expected):
    model_inputs = std_input_cases[0].copy()
    for item, value in input_data.items():
        model_inputs[item] = value

    with pytest.raises(expected):
        Inputs(**model_inputs)


# NOTE: This test is commented out to avoid real API calls to wikidata during 
# regular test runs.
# It should only be uncommented and run if changes are made to the `Cities`
# class that affect API behavior. Use caution and consider mocking the API 
# call instead as done in the base_ModelLogInput redefiniton in 
# /tests/mlflow_client/conftest.py:
# [Cities.model_construct(**city) for city in std_model_cases[0]['cities']]

# def test_cities_success():
#     city_case = std_model_cases[0]['cities'][0]
#     city = Cities(wikidata_id=city_case['wikidata_id'])

#     assert city.name == city_case['name']
#     assert city.country == city_case['country']
#     assert city.hierarchy == city_case['hierarchy']


def test_ModelLogInput_success():
    model_log_input = ModelLogInput(**base_ModelLogInput)
    assert isinstance(model_log_input, ModelLogInput)


@pytest.mark.parametrize(
    'input_data, expected',
    [
        # No model
        ({'model': None}, TypeError),
        # x_test size != 100
        ({'x_test': pd.DataFrame(
            {"Column_1": [1]})}, ValueError),
        # y_test size != 100
        ({'y_test': np.array([1])}, ValueError),
        # date_year > current year
        ({'data_year': datetime.now().year + 1}, ValueError),
        # Input column name is not a X column
        ({'inputs': [Inputs(**{**std_input_cases[0], 'column_name': 'not in X'})]}, ValueError)
    ]
)
def test_ModelLogInput_error(input_data, expected):
    model_inputs = base_ModelLogInput.copy()
    for item, value in input_data.items():
        model_inputs[item] = value

    with pytest.raises(expected):
        ModelLogInput(**model_inputs)


def test_prepare_json(modelLogInput_instance):
    json_model = modelLogInput_instance._prepare_json('id')
    assert json_model['id'] == 'id'


def test_generate_zip_success(modelLogInput_instance):
    folder_path = modelLogInput_instance.generate_zip()
    assert pathlib.Path(f'{folder_path}.zip').is_file()
