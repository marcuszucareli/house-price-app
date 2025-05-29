"""
client.py

This module defines clients for interacting with the MLflow API. Includes:

- APIClientInterface: Abstract base class defining the interface and common
errors.
- MlflowAPI: Client for interacting with the production MLflow API.
- MockAPI: Mock client used for development and testing.

Author: Marcus Zucareli
Date: 2025-05-29
"""

import os
import requests
import json
from mlflow.entities.model_registry import RegisteredModel

class APIClientInterface:
    def get_models(self) -> list[RegisteredModel]:
        """
        Fetch registered models from the Mlflow API.

        Raises:
            NotImplementedError: This method must be overridden in subclasses.
        """
        raise NotImplementedError('get_models not implemented in this class.')

class MlflowAPI(APIClientInterface):
    def get_models(self) -> list[RegisteredModel]:
        """
        Fetch registered models from the Mlflow API.

        Returns:
            List[RegisteredModel]: A list of registered models fetched from the
            MLflow API.
        """
        API_BASE_URL = os.getenv('API_BASE_URL')
        url = f'{API_BASE_URL}'
        res = [url]
        return res

class MockAPI(APIClientInterface):
    def __init__(self):
        import time
        from mlflow.entities.model_registry import RegisteredModelTag

        inputs = {
            'neighbourhood': {
                'name': 'Neighbourhood',
                'type': 'categorical',
                'options': ['1 arrondissement', '2 arrondissement'],
            },
            'is_new': {
                'name': 'Old or New?',
                'type': 'bool',
                'options': None
            },
            'n_bedrooms': {
                'name': 'Number of Bedrooms',
                'type': 'int',
                'options': None
            },
            'square': {
                'name': 'Size (m²)',
                'type': 'float',
                'options': None
            },
        }
    
        self._mock_model_1 = RegisteredModel(
            name="mock_model",
            creation_timestamp=1234567890,
            last_updated_timestamp=1234567899,
            description="Mock model 1",
            latest_versions=[],
            tags=[
                RegisteredModelTag(key="country", value="Brazil"),
                RegisteredModelTag(key="cities", value=json.dumps(["São José dos Campos", "Jacareí", "Taubaté"])),
                RegisteredModelTag(key="author", value="Santos Dumont"),
                RegisteredModelTag(key="algorithm", value="Random Forest"),
                RegisteredModelTag(key="data_year", value=2025),
                RegisteredModelTag(key="inputs", value=json.dumps(inputs))
            ],
            aliases=[]
        )

        self._mock_model_2 = RegisteredModel(
            name="mock_model",
            creation_timestamp=1234567890,
            last_updated_timestamp=1234567899,
            description="Mock model 2",
            latest_versions=[],
            tags=[
                RegisteredModelTag(key="country", value="France"),
                RegisteredModelTag(key="cities", value=json.dumps(["Paris", "Lyon"])),
                RegisteredModelTag(key="author", value="Edith Piaf"),
                RegisteredModelTag(key="algorithm", value="Boosting"),
                RegisteredModelTag(key="data_year", value=2023),
                RegisteredModelTag(key="inputs", value=json.dumps(inputs))
            ],
            aliases=[]
        )


    def get_models(self) -> list[RegisteredModel]:
        """
        Simulate the `get_models` method of MlflowAPI for development and
        testing purposes.

        Returns:
            list[RegisteredModel]: A list of mocked MLflow registered models.
        """
        return [self._mock_model_1, self._mock_model_2]