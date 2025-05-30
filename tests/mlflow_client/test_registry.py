import pytest
from mlflow_client.registry import Models

def test_get_places(monkeypatch):
    monkeypatch.setenv('ENV', 'dev')
    models = Models()
    places = models.get_places()

    assert isinstance(places, dict)
    assert isinstance(places['Brazil'], list)
    assert places['Brazil'] == ["Jacareí", "São José dos Campos", "Taubaté"]
    assert places['France'] == ["Lyon", "Paris"]
    assert list(places.keys()) == ['Brazil', 'France']