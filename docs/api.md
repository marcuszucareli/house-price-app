# API

## About the module
The API module is responsible for serving a REST API for consulting available models and predicting real estate prices.

## Endpoints
Endpoints, schemas and examples can be found in the api documentation. you can also live test them.
- [documentation](https://api.home-estimate-ai.uk/redoc)
- [live test](https://api.home-estimate-ai.uk/docs)
- [documentation (local host)](http://localhost:8000/redoc)
- [live test (local host)](http://localhost:8000/docs)

## Running

The api service is automatically run on port 8000 by docker-compose when starting the container, if you need to stop and start it again for any reason, use the command bellow on the api container:

```bash
uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload
```