import pytest
import os
import zipfile
from tests.conftest import standard_uuid


@pytest.fixture
def storage(monkeypatch, tmp_path):
    storage_path = tmp_path / 'storage'
    monkeypatch.setenv("STORAGE_PATH", str(storage_path))

    zip_source_path = f'tests/data/{standard_uuid}.zip'
    zip_destination_path = str( storage_path / str(standard_uuid))
    
    os.makedirs(zip_destination_path, exist_ok=True)

    with zipfile.ZipFile(zip_source_path, 'r') as zip:
            zip.extractall(zip_destination_path)
    
    yield storage_path
    
    
@pytest.fixture
def client(temp_db_path, storage):
    from fastapi.testclient import TestClient
    from api.api import app

    client = TestClient(app)

    yield client