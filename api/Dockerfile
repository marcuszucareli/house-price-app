FROM python:3.13-slim

WORKDIR /service

COPY ./requirements/lock.txt lock_requirements.txt
COPY ./requirements/api.txt requirements.txt

RUN pip install --no-cache-dir -r lock_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api
COPY ./database ./database
COPY ./tests/__init__.py ./tests/__init__.py
COPY ./tests/api ./tests/api
COPY ./tests/database ./tests/database
COPY ./tests/conftest.py ./tests/conftest.py

EXPOSE 8000
