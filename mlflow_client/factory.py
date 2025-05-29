import os
from mlflow_client.client import MlflowAPI, MockAPI


def get_mlflow_client():
    ENV = os.getenv('ENV')
    return MlflowAPI() if ENV == 'prod' else MockAPI()
