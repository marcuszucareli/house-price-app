import pytest
from mlflow_client.client import MlflowAPI, MockAPI
from mlflow.entities.model_registry import RegisteredModel
import json

def test_get_models(monkeypatch):
    API_BASE_URL = 'test_base_url'
    cities = json.dumps(["São José dos Campos", "Jacareí", "Taubaté"])
    monkeypatch.setenv('API_BASE_URL', API_BASE_URL)

    mlflowAPI = MlflowAPI()
    mockAPI = MockAPI()

    mlflowAPI_response = mlflowAPI.get_models()
    mock_response = mockAPI.get_models()

    # Testing mock
    assert isinstance(mock_response, list)
    assert isinstance(mock_response[0], RegisteredModel)
    assert mock_response[0].tags['country'] == 'Brazil'
    assert mock_response[0].tags['cities'] == cities
