import pytest
import pandas as pd
import numpy as np
import pathlib
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from mlflow_client.model_logging import Inputs, ModelLogInput, max_chars

# Define a test regression model
X = pd.DataFrame(
    data={
        'column_1': [i for i in range(100)]
    }
)
y = np.array([i for i in range(100)])
test_model = LinearRegression()
test_model.fit(X, y)

# Define base model input
base_ModelLogInput = {
    'model': test_model,
    'model_link': 'https://www.santosfc.com.br/',
    'flavor': 'sklearn',
    'x_test': pd.DataFrame(
        {
            "column_1": [i for i in range(100)]
        }
    ),
    'y_test': np.array([i for i in range(100)]),
    'author': 'Edson Arantes do Nascimento',
    'algorithm': 'regression',
    'data_year': 2025,
    'country': 'Brazil',
    'cities': ['Belo Horizonte', 'Contagem'],
    'inputs': [
        Inputs(
            **{
                'column_name': "column_1",
                'label': "Your input",
                'type': "int",
                'options': [],
                'description': 'Number you want to multiply by 2',
                'unit': None
            }
        )
    ],
    'links': {
        'Github': 'https://github.com/marcuszucareli',
        'Linkedin': 'https://www.linkedin.com/feed/'
    }
}

# Define the wrong input class
base_Inputs = {
    'column_name': "is_new",
    'label': "Is your house new?",
    'type': "bool",
    'options': [],
    'description': 'If you house has less than 5 years',
    'unit': None
}
wrong_input = base_Inputs.copy()
wrong_input['column_name'] = 'Not in x_test'


@pytest.mark.parametrize(
    "input_data, expected",
    [   
        # Type bool
        (
            {
                'column_name': "is_new",
                'label': "Is your house new?",
                'type': "bool",
                'options': [],
                'description': 'If you house has less than 5 years',
                'unit': None
            },
            Inputs
        ),
        # Type int
        (
            {
                'column_name': "n_bedrooms",
                'label': "Number of bedrooms in the house",
                'type': "int",
                'options': [],
                'description': '',
                'unit': 'un'
            },
            Inputs
        ),
        # Type float
        (
            {
                'column_name': "m2",
                'label': "area_m2",
                'type': "float",
                'options': [],
                'description': 'The property size in m².',
                'unit': 'm²'
            },
            Inputs
        ),
        # Type categorical
        (
            {
                'column_name': "neighbourhood",
                'label': "Neighbourhood",
                'type': "categorical",
                'options': ['Morumbi', 'América'],
                'description': 'Property neighbourhood',
                'unit': None
            },
            Inputs
        )
    ]
)
def test_Inputs_validation_success(input_data, expected):
    model_input = Inputs(**input_data)
    assert isinstance(model_input, expected)


@pytest.mark.parametrize(
    "input_data, expected",
    [   
        # column_name string size
        ({'column_name': "a"*(max_chars+1)}, ValueError),
        # label string size
        ({'label': "a"*(max_chars+1)}, ValueError),
        # not listed type
        ({'type': "a"}, ValueError),
        # Only one option
        ({'options': ['Morumbi'],
          'type': 'category'
          }, ValueError),
        # Description string size
        ({'description': "a"*250}, ValueError),
        # unit string size
        ({'unit': "a"*(max_chars+1)}, ValueError)
    ]
)
def test_Inputs_validation_error(input_data, expected):
    model_inputs = base_Inputs.copy()
    for item, value in input_data.items():
        model_inputs[item] = value

    with pytest.raises(expected):
        Inputs(**model_inputs)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (base_ModelLogInput, ModelLogInput)
    ]
)
def test_ModelLogInput_success(input_data, expected):
    model_log_input = ModelLogInput(**input_data)
    assert isinstance(model_log_input, expected)


@pytest.mark.parametrize(
    'input_data, expected',
    [
        ({'model': None}, TypeError),   # No model
        ({'x_test': pd.DataFrame( \
            {"Column_1": [1]})}, ValueError),   # x_test size != 100
        ({'y_test': np.array([1])}, ValueError),   # y_test size != 0
        ({'data_year': \
          datetime.now().year + 1}, ValueError),   # date_year > current year
        ({'inputs': [Inputs(**wrong_input)]}, ValueError)   # Wrong input
    ]
)
def test_ModelLogInput_error(input_data, expected):
    model_inputs = base_ModelLogInput.copy()
    for item, value in input_data.items():
        model_inputs[item] = value

    with pytest.raises(expected):
        ModelLogInput(**model_inputs)


@pytest.mark.parametrize(
    "input_data",
    [
        (base_ModelLogInput)
    ]
)
def test_generate_zip_success(input_data):
    model_log_input = ModelLogInput(**input_data)
    model_log_input.generate_zip('test_model')

    assert pathlib.Path('./model_development/test_model.zip').is_file()
    os.remove('./model_development/test_model.zip')

