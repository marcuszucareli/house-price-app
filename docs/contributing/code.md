#  😃 Welcome!

Thanks for contributing to the project! If you’re here, it means you’ve already [set up your development environment](../../README.md#getting-started-locally). This document outlines the process and conventions we follow to keep development organized and consistent.

## About the development environment

If you use the suggested setup for development, you might notice that, while inside the devcontainer, not all files of the codebase are visible. This is because we mimic the production scenario, where each container is isolated from the others. This helps avoid compatibility issues between development and production, but requires a bit of attention:

The default service in the development environment is `mlflow_client`. You can switch to another service you want to work on by changing the service parameter in the `devcontainer.json`.

>⚠️ Note: You **must not** commit changes on `devcontainer.json`. Adjust it locally to match your workflow, but these modifications are personal and shouldn’t be pushed to the repository.

```json
{
  "name": "housing-estimate-ai",
  "dockerComposeFile": "../docker-compose.dev.yml",
  "service": "mlflow_client", // You can choose between `api` and `app`
  "workspaceFolder": "/service",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "ms-toolsai.jupyter"
      ]
    }
  },
  "forwardPorts": [8000, 8080]
}
```

Bellow, we list the modules that each service has access to. You can check the full list of volumes for each service in the [docker-compose.dev file](../../docker-compose.dev.yml)

**app**
- app

**api**
- api
- database
- tests/api
- tests/databse

**mlflow_client**
- mlflow_client
- database
- tests/mlflow_client
- tests/databse

If you need to do a quick change in another service while working in other one, you can open a second window with the local version of the codebase and change it there. Use this workaround **only for simple things** such as docs.

## A brief note on terminals (for those not familiar with docker)

> ⚠️ **Note on terminals:**  
> 
> By default, the Dev Container opens a terminal for the `mlflow_client` service.  
> 
> If you want to interact with other services, you can find the container ID for the desired service and open a terminal inside it using:
> ```bash
> # Finding containers id
> docker ps
>
>CONTAINER ID   ...   PORTS                    NAMES
>e54ce2ee158c   ...   0.0.0.0:8080->8080/tcp   house-price-app-app-1
>ab043062a750   ...   0.0.0.0:8000->8000/tcp   house-price-app-api-1
>7c67fd024462   ...   0.0.0.0:5000->5000/tcp   house-price-app-mlflow_client-1
>
> # Creating the terminal
> docker exec -it <container_id> bash
> ```
> If you are `using Docker Compose`, this is the way to open terminals to interact with the services environments.

## 📋 Summary
- [🐛 Reporting issues](#🐛-reporting-issues)
- [🔀 Pull requests](#🔀-pull-requests)
- [🌿 Branching Model](#🌿-branching-model)
- [🧑‍💻 Commit Messages](#🧑‍💻-commit-messages)
- [✅ Tests](#✅-tests)
- [📄 Code Style](#📄-code-style)

## 🐛 Reporting Issues

To report an issue, simply fill the [bugs template](https://github.com/marcuszucareli/house-price-app/issues/new?template=bug_report.md).

## 🔀 Pull Requests

- In your forked repository, create a new branch from main.
- Follow commit and branch naming conventions (see below).
- Make sure all tests pass before submitting.
- Write clear and descriptive PR titles.
- Allow `edits from maintainers` when creating the PR

## 🌿 Branching Model

We follow a simplified GitHub Flow based on project services (`api`, `app`, `mlflow_client` and for more abrangent purposes `general`):

- main → stable branch (production-ready code).
- feature/service_name/xxx → for new features.
- fix/service_name/xxx → for bug fixes.
- docs/service_name/xxx → for documentation updates.

## 🧑‍💻 Commit Messages

We follow Conventional Commits:

- feat: → new features
- fix: → bug fixes
- docs: → documentation changes
- test: → adding or updating tests
- refactor: → code refactoring without changing functionality

Example:

- feat: add user authentication endpoint
- fix: correct SQLite connection error
- docs: add setup instructions

## ✅ Tests

- Always add or update tests for new features or bug fixes.
- Run the test suite locally before submitting PRs.
- Keep test cases isolated and descriptive.

### Running tests
We use [Pytest](https://docs.pytest.org/en/stable/) to write and run our tests, so simply execute `pytest` to run them.

```bash
pytest
```

> ⚠️ **Note:** Remember that `app`, `api` and `mlflow_client` services are in independent environments, so you need to **run pytest in all of them**

## 📄 Code Style

Project must follow [PEP8](https://peps.python.org/pep-0008/).


