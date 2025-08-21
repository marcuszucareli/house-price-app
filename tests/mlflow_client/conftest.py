import pytest
import pandas as pd
import numpy as np
import os
import zipfile
import shutil
import json
from sklearn.linear_model import LinearRegression
from mlflow_client.model_logging import Inputs, Cities
from mlflow_client.config import MODEL_JSON_NAME
from tests.conftest import std_input_cases, standard_uuid, std_model_cases

# ########################
# Variables and functions
# ########################

# Returns a generic scikit-learn model object
def scikit_model():
    data = {}
    for input_case in std_input_cases:
        if input_case['type'] == 'map': 
            data[input_case['lat']] = [i for i in range(100)]
            data[input_case['lng']] = [i for i in range(100)]
        else:
            data[input_case['column_name']] = [i for i in range(100)]
    
    # X features using all input cases
    X = pd.DataFrame(data=data)

    # Define a test regression model
    y = np.array([i for i in range(100)])
    model = LinearRegression()
    model.fit(X, y)

    return model, X, y


# Define a base input to create a ModelLogInput class
generic_model, X_generic_model, y_generic_model = scikit_model()
base_ModelLogInput = {
     **std_model_cases[0],
    'model': generic_model,
    'x_test': X_generic_model,
    'y_test': y_generic_model,
    'inputs': [Inputs(**args) for args in std_input_cases],
    'cities': [
         Cities.model_construct(**city) \
            for city in std_model_cases[0]['cities']]
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
    print(base_ModelLogInput['x_test'])
    return ModelLogInput(**base_ModelLogInput)


# Set up environment for ingestion tests (db, ingestion and storage)
@pytest.fixture
def ingestion_flow_env(monkeypatch, tmp_path, temp_db_path):

    ingestion_path = tmp_path / 'ingestion'
    storage_path = tmp_path / 'storage'
    unpacked_file_path = tmp_path / 'unpacked'

    monkeypatch.setenv("INGESTION_PATH", str(ingestion_path))
    monkeypatch.setenv("STORAGE_PATH", str(storage_path))

    os.makedirs(str(ingestion_path))
    os.makedirs(str(storage_path))
    os.makedirs(str(unpacked_file_path))

    zip_source_path = f'tests/data/{standard_uuid}.zip'
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
