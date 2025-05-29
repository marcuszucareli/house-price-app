import os
import requests
import json

class APIClientInterface:
    def get_models(self) -> list:
        raise NotImplementedError('get_models not implemented')

class MlflowAPI(APIClientInterface):
    def get_models(self) -> list:
        API_BASE_URL = os.getenv('API_BASE_URL')
        url = f'{API_BASE_URL}'
        res = [url]
        return res

class MockAPI(APIClientInterface):
    def __init__(self):
        import time
        from mlflow.entities.model_registry import RegisteredModel, RegisteredModelTag

        self._mock_model_1 = RegisteredModel(
            name="mock_model",
            creation_timestamp=1234567890,
            last_updated_timestamp=1234567899,
            description="Mock model 1",
            latest_versions=[],
            tags=[
                RegisteredModelTag(key="country", value="Brazil"),
                RegisteredModelTag(key="city", value=json.dumps(["São José dos Campos", "Jacareí", "Taubaté"]))
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
                RegisteredModelTag(key="city", value=json.dumps(["Paris"]))
            ],
            aliases=[]
        )


    def get_models(self) -> list:
        return [self._mock_model_1, self._mock_model_2]