# APP

## About the module
The APP module is a streamlit application to allow real estate prices predictions using a web interface.

## Client
The client file defines a class to interact with the API and manage/clean states according to user inputs in the web app.

## Web App
The main file controls the streamlit home page and is responsible for consulting countries, models and the necessary inputs to predict properties values for each model. Models' inputs are rendered under a form as follow:

| Input Type  | Widgets         |
| ----------- | ----------      |
| int         | number input    |
| float       | number input    |
| bool        | toggle          |
| categorical | selectbox       |
| map         | folium map      |

The results page serves a primarily expository role. Apart from links and a button to navigate back to the main page, it does not involve user interaction.

## Translations 
Translations uses a simple dictionary to retrieve the texts from the corresponding user language. Any text add must be translated to the idioms already implemented.

## API consulting
The web app uses the docker network to consult the API.

## Running
The app service is automatically run on port 8080 by docker-compose when starting the container, if you need to stop and start it again for any reason, use the command bellow on the app container:

```bash
streamlit run ./app/main.py --server.port=8080 --server.address=0.0.0.0
```