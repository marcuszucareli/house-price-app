"""
factory.py

Defines the classes, connections, and functions to be used depending on
the environment (development or production).

Author: Marcus Zucareli
Date: 2025-05-29
"""

import os
from mlflow_client.client import MlflowAPI, MockAPI


def get_mlflow_client() -> MlflowAPI | MockAPI:
    """
    Define Mlflow client class depending on the environment.

    Returns:
        MlflowAPI | MockAPI: An instance of the class based on the environment.
    """
    ENV = os.getenv('ENV')
    return MlflowAPI() if ENV == 'prod' else MockAPI()
