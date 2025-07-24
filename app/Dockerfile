FROM python:3.13-slim

ARG APP_ENV

WORKDIR /service

COPY ./requirements/app.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./.streamlit/config.${APP_ENV}.toml .streamlit/config.toml
COPY ./app ./app

EXPOSE 8080

ENV PYTHONPATH=. 
