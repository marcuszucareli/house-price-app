import pytest
import pandas as pd
import numpy as np
import pathlib
import uuid
from datetime import datetime
from mlflow_client.model_logging import Inputs, ModelLogInput, max_chars
from tests.mlflow_client.conftest import input_cases, base_ModelLogInput




@pytest.mark.parametrize("input_data", input_cases)
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
        # Map type and column_name is string
        ({'type':"map", 'column_name':'string'}, ValueError),
        # Map type and column_name list has size != 2
        ({'type':"map", 'column_name':['string']}, ValueError)
    ]
)
def test_Inputs_validation_error(input_data, expected):
    model_inputs = input_cases[0].copy()
    for item, value in input_data.items():
        model_inputs[item] = value

    with pytest.raises(expected):
        Inputs(**model_inputs)


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
        ({'inputs': [Inputs(**{**input_cases[0], 'column_name': 'not in X'})]}, ValueError)
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
