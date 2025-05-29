import pytest
from mlflow_client.factory import get_mlflow_client
from mlflow_client.client import MlflowAPI, MockAPI

@pytest.mark.parametrize("env", ['dev', 'prod'])
def test_get_mlflow_client(monkeypatch, env):
    monkeypatch.setenv('ENV', env)
    mlflow_client_class = get_mlflow_client()
    if env == 'dev':
        assert isinstance(mlflow_client_class, MockAPI)
    else:
        assert isinstance(mlflow_client_class, MlflowAPI)
