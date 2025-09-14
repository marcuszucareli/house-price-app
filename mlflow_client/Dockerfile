FROM python:3.13-slim

WORKDIR /service

COPY ./requirements/lock.txt lock_requirements.txt
COPY ./requirements/mlflow_client.txt requirements.txt

RUN pip install --no-cache-dir -r lock_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./mlflow_client ./mlflow_client
COPY ./database ./database
COPY ./tests/__init__.py ./tests/__init__.py
COPY ./tests/mlflow_client ./tests/mlflow_client
COPY ./tests/database ./tests/database
COPY ./model_development ./model_development
COPY ./tests/conftest.py ./tests/conftest.py

EXPOSE 5000

ENV PYTHONPATH=. 
