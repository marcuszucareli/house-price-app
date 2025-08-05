import pytest
import pandas as pd
import numpy as np
import uuid
import os
import zipfile
import shutil
import json
from sklearn.linear_model import LinearRegression
from mlflow_client.model_logging import Inputs
from mlflow_client.config import MODEL_JSON_NAME

# ########################
# Variables and functions
# ########################

# Define cases to test/create instances of Input classe
input_cases = [   
    # Type bool
    {
        'column_name': "is_new",
        'lat': "lat",
        'lng': "lng",
        'label': "Is your house new?",
        'type': "bool",
        'options': [],
        'description': 'If your house has less than 5 years',
        'unit': None
    },
    # Type int
    {
        'column_name': "n_bedrooms",
        'lat': "lat",
        'lng': "lng",
        'label': "Number of bedrooms in the house",
        'type': "int",
        'options': [],
        'description': '',
        'unit': 'un'
    },
    # Type float
    {
        'column_name': "m2",
        'lat': "lat",
        'lng': "lng",
        'label': "area_m2",
        'type': "float",
        'options': [],
        'description': 'The property size in m².',
        'unit': 'm²'
    },
    # Type categorical
    {
        'column_name': "neighbourhood",
        'lat': "lat",
        'lng': "lng",
        'label': "Neighbourhood",
        'type': "categorical",
        'options': ['Morumbi', 'América'],
        'description': 'Property neighbourhood',
        'unit': None
    },
    # Type maps
    {
        'column_name': 'map',
        'lat': 'latitude',
        'lng': 'longitude',
        'label': "Coordinates",
        'type': "map",
        'options': [],
        'description': "house's Latitude and Longiude",
        'unit': None
    }
]

# Define standard UUID for file names
standard_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")


# Returns a generic scikit-learn model object
def scikit_model():
    data = {}
    for input_case in input_cases:
        data[input_case['column_name']] = [i for i in range(100)]
    
    data['column_1'] = [i for i in range(100)]

    # An X just to model a simple regression (wont be used to tests validation)
    X = pd.DataFrame(
        data=data
    )

    # X features using all input cases
    # X = pd.DataFrame(data=X)

    # Define a test regression model
    y = np.array([i for i in range(100)])
    model = LinearRegression()
    model.fit(X, y)

    return model, X, y


# Define a base input to create a ModelLogInput class
generic_model, X_generic_model, y_generic_model = scikit_model()
base_ModelLogInput = {
    'model': generic_model,
    'model_link': 'https://www.santosfc.com.br/',
    'flavor': 'sklearn',
    'x_test': X_generic_model,
    'y_test': y_generic_model,
    'author': 'Edson Arantes do Nascimento',
    'algorithm': 'Regression',
    'data_year': 2025,
    'country': 'Brazil',
    'cities': ['Belo Horizonte', 'Três Corações'],
    'inputs': [Inputs(**args) for args in input_cases],
    'links': {
        'Github': 'https://github.com/',
        'Linkedin': 'https://www.linkedin.com/'
    }
}


# ########################
# Fixtures
# ########################

# Returns a ModelLogInput object with all the Input Cases
@pytest.fixture
def modelLogInput_instance(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "mlflow_client.model_logging.uuid.uuid4",
        lambda: standard_uuid
    )
    monkeypatch.setattr(
        "mlflow_client.model_logging.DEV_FOLDER_PATH", tmp_path)

    from mlflow_client.model_logging import ModelLogInput

    return ModelLogInput(**base_ModelLogInput)


# Set up environment for ingestion tests (db, ingestion and storage)
@pytest.fixture
def ingestion_flow_env(monkeypatch, tmp_path, temp_db_path):

    ingestion_path = tmp_path / 'ingestion'
    storage_path = tmp_path / 'storage'
    unpacked_file_path = tmp_path / 'unpacked'

    monkeypatch.setenv("INGESTION_PATH", str(ingestion_path))
    monkeypatch.setenv("STORAGE_PATH", str(storage_path))
    monkeypatch.setenv("DB_PATH", str(temp_db_path))

    os.makedirs(str(ingestion_path))
    os.makedirs(str(storage_path))
    os.makedirs(str(unpacked_file_path))

    zip_source_path = f'tests/mlflow_client/data/{standard_uuid}.zip'
    zip_destination_path = f'{unpacked_file_path}/{standard_uuid}.zip'
    shutil.copy(zip_source_path, zip_destination_path)

    with zipfile.ZipFile(zip_destination_path, 'r') as zip:
            zip.extractall(unpacked_file_path)
    
    with open(
            f'{unpacked_file_path}/{MODEL_JSON_NAME}', 'r', encoding='utf-8') \
            as f:
            std_json = json.load(f)

    yield ingestion_path, storage_path, temp_db_path, \
        unpacked_file_path, std_json, standard_uuid
