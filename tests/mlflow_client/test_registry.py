import pytest
from mlflow_client.registry import get_places

def test_get_places(monkeypatch):
    monkeypatch.setenv('ENV', 'dev')
    places = get_places()

    assert isinstance(places, dict)
    assert isinstance(places['Brazil'], list)
    assert places['Brazil'] == ["Jacareí", "São José dos Campos", "Taubaté"]
    assert places['France'] == ["Paris"]
    assert list(places.keys()) == ['Brazil', 'France']