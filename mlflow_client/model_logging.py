import pandas as pd
import numpy as np
import mlflow.pyfunc
import tempfile
import shutil
import json
import uuid
import requests
from pydantic import BaseModel
from dataclasses import field
from typing import Optional, Any
from datetime import datetime
from sklearn.metrics import  r2_score, root_mean_squared_error, \
    mean_absolute_percentage_error, mean_absolute_error
from mlflow_client.config import MODEL_FOLDER_NAME, MODEL_JSON_NAME, \
    DEV_FOLDER_PATH
from database.init_db import init_db

# Define the maximum number of chars in strings
max_chars = 64
WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": \
        "MyGeoApp/0.1 (https://github.com/marcuszucareli/house-price-app)"
}

class Inputs(BaseModel):
    """
    Defines the necessary parameters that each input of the model should have.

    Args:
        column_name (str): The column name in the model. 
        lat (str): column name for the latitude parameter in the model when 
        using type `map`.
        lng (str): column name for the longitude parameter in the model when 
        using type `map`.
        label (str): The name to be displayed in the Streamlit app.
        type (str): The type of the input. Must be one of the following
                    options:
            - "bool": A boolean parameter.
            - "int": An int parameter.
            - "float": An float parameter.
            - "categorical": A categorical parameter. If choosing "categorical"
                you must specify the options attribute.
            - "map": A lat and lng coordinate rendered as a map.
        options (list[str]): The options of the categorical parameter.
        description (Optional[str] = None, optional): A brief description of 
        the parameter.
        unit (Optional[str] = None, optional): Unit of measurement associated 
        with the parameter.
    """
    model_config = {
        "arbitrary_types_allowed": True
    }
    column_name: str
    lat: str = None
    lng: str = None
    label: str
    type: str
    options: Optional[list[str]] = field(default_factory=list)
    description: Optional[str] = ''
    unit: Optional[str] = ''


    def model_post_init(self, __context):
        allowed_data_types = ['bool', 'int', 'float', 'categorical', 'map']
        if len(self.column_name) > max_chars:
            raise ValueError("column_name cannot be longer than 64 characters")
        
        if len(self.label) > max_chars:
            raise ValueError("label cannot be longer than 128 characters")
        
        if self.type not in allowed_data_types:
            error_message = "type must be one of the following strings"
            data_types = ', '.join(allowed_data_types)
            raise ValueError(f"{error_message} {data_types}")
        
        if self.type == 'categorical':
            if len(self.options) < 2:
                raise ValueError(
                    "Categorical variables require the available " \
                    "options to be defined.")
        
        if self.type == 'map':
            if self.lat is None or self.lng is None:
                raise ValueError("You must set lat and lng parameters when " \
                "creating a map input.")

        if isinstance(self.description, str) and \
            len(self.description) > 200:
            raise ValueError("label cannot be longer than 128 characters")
        
        if isinstance(self.unit, str) and \
            len(self.unit) > max_chars:
            raise ValueError("label cannot be longer than 128 characters")


class Cities(BaseModel):
    """
    Represents a city with its Wikidata ID, name, country, and administrative 
    hierarchy.

    Args:
        wikidata_id (str): QID of the city in 
        [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) (e.g., 
        "Q1297" for Chicago)
        name (str): Name of the city in English
        country (str): Name of the country in English
        hierarchy (List[str]): List of administrative divisions from closest 
        to city to most general, excluding the country
    """

    wikidata_id: str
    name: str = ''
    country: str = ''
    hierarchy: str = ''

    def model_post_init(self, context):
            self.get_data()
            if self.name == '' or self.country == '':
                raise ValueError(f"Failed to initialize Cities instance.")

    def get_data(self):
        # Try to fetch all data; if any fails, raise exception
        try:
            self.name = self._get_label(self.wikidata_id)
            if not self.name:
                raise ValueError(
                    f"City label not found for QID {self.wikidata_id}")
            
            self.country = self._get_country()
            if not self.country:
                raise ValueError(
                    f"Country not found for QID {self.wikidata_id}")
            
            self.hierarchy = self._get_hierarchy()
        
        except Exception as e:
            # Prevent creation of invalid instance
            raise ValueError(f"Failed to initialize Cities instance: {e}")

    def _get_label(self, qid: str) -> str:
        """Returns the English label for a Wikidata entity."""
        query = f"""
        SELECT ?label WHERE {{
          wd:{qid} rdfs:label ?label .
          FILTER(LANG(?label) = "en")
        }}
        """
        response = requests.get(
            WIKIDATA_SPARQL_URL, params={"query": query}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", {}).get("bindings", [])
        return results[0]["label"]["value"] if results else ""

    def _get_country(self) -> str:
        """Fetches the country name from Wikidata using P17."""
        query = f"""
        SELECT ?country WHERE {{
          wd:{self.wikidata_id} wdt:P17 ?country .
        }}
        """
        response = requests.get(
            WIKIDATA_SPARQL_URL, params={"query": query}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        country_qid = \
            data["results"]["bindings"][0]["country"]["value"].split("/")[-1]
        return self._get_label(country_qid)

    def _get_hierarchy(self) -> list[str]:
        """
        Returns a simplified hierarchy: [City Name, Main Administrative 
        Division (state/province/region)].
        """
        query = f"""
        SELECT ?admin WHERE {{
          wd:{self.wikidata_id} wdt:P131 ?admin .
        }} LIMIT 1
        """
        response = requests.get(
            WIKIDATA_SPARQL_URL, params={"query": query}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        bindings = data.get("results", {}).get("bindings", [])

        if bindings:
            admin_qid = bindings[0]["admin"]["value"].split("/")[-1]
            admin_label = self._get_label(admin_qid)
            return admin_label
        else:
            # No administrative division found
            return ''


class ModelLogInput(BaseModel):
    """
    Validates model information to ensure compliance with the project's 
    standards.
    
    Args:
        model (Any): A machine learning model compatible with the MLflow 
        library.
        model_link (str): The link to download the Mlflow registered model. 
        The MLflow download link must be provided via a reputable file-sharing 
        or cloud storage platform (e.g., Google Drive, Dropbox, or OneDrive) to
         ensure reliable access and security.
        flavor (str): The library used to create the model. Must be one of the 
        following options:
            - "sklearn"
            - "xgboost"
            - "lightgbm"
            - "keras"
            - "tensorflow"
        x_test (pd.DataFrame): A sample of 100 rows from the model's test
         data, used for validation and logging.
        y_test (pd.Series | np.ndarray): The lable value associated with the
         x_test data, used for validation and logging.
        author (Optional[str], optional): The author of the model
        algorithm (str): The algorithm used to train the model (e.g., linear 
        regression, random forest, XGBoost, etc.).
        data_year (int): The earliest year of the data used to train the model.
        cities (list[Cities]): List of cities related to the data, each 
        represented as an instance of the City class.
        inputs (list[Inputs]): List of user-provided inputs required to make 
        a prediction. Do not include feature engineering parameters—this list 
        should contain only the inputs explicitly required from the user.
        links (Optional[(dict[str]], optional): A dict of usefull URL's for the
         model. Use it to
        share notebooks, Github pages, Linkedin and other resources. Theses
        links wiil be displayed in the bottom of the Streamlit application.

     Attributes:
        mape (float | int): Mean Absolute Percentage Error of the model in 
        decimal form.
        mae (float | int): Mean Absolute Error of the model.
        rmse (float | int): Root Mean Squared Error of the model.
        r2 (float | int): R-squared of the model
    """
    # Set pydantic configs
    model_config = {"arbitrary_types_allowed": True}

    # Model
    model: Any
    model_link: str
    flavor: str

    # Metrics
    r2: Optional[float] = None
    mae: Optional[float] = None
    mape: Optional[float] = None
    rmse: Optional[float] = None

    # Artefacts
    x_test: pd.DataFrame
    y_test: pd.Series | np.ndarray

    # Tags
    algorithm: str
    data_year: int
    cities: list[Cities]
    inputs: list[Inputs]
    author: Optional[str] = None
    links: Optional[dict[str, str]] = [{}]


    def _save_model(self, save_dir):
        match self.flavor:
                case "sklearn":
                    import mlflow.sklearn
                    mlflow.sklearn.save_model(
                            sk_model=self.model,
                            path=save_dir
                        )

                case "xgboost":
                    import mlflow.xgboost
                    mlflow.xgboost.save_model(
                        xgb_model=self.model,
                        path=save_dir
                    )

                case "lightgbm":
                    import mlflow.lightgbm
                    mlflow.lightgbm.save_model(
                        lgbm_model=self.model,
                        path=save_dir
                    )

                case "catboost":
                    import mlflow.catboost
                    mlflow.catboost.save_model(
                        model=self.model,
                        path=save_dir
                    )

                case "keras" | "tensorflow":
                    import mlflow.keras
                    mlflow.keras.save_model(
                        keras_model=self.model,
                        path=save_dir
                    )

                case _:
                    raise ValueError('Model type not supported.')


    def get_metrics(self):
        # Validate x_test
        if len(self.x_test) != 100:
            raise ValueError("x_test must have 100 lines")
        # Validate y_test
        if len(self.y_test) != 100:
            raise ValueError("y_test must have 100 lines")

        with tempfile.TemporaryDirectory() as tmp_dir:
            mlflow.set_tracking_uri(f"file://{tmp_dir}")
            model_path = f'{tmp_dir}/{MODEL_FOLDER_NAME}'
            # Save the model
            self._save_model(model_path)
            
            # Load model using pyfunc
            model_loaded = mlflow.pyfunc.load_model(model_path)

            # predict
            y_test_repository = model_loaded.predict(self.x_test)
        
        # Calculate metrics
        self.r2 = r2_score(self.y_test, y_test_repository)
        self.rmse = root_mean_squared_error(self.y_test, y_test_repository)
        self.mae = mean_absolute_error(self.y_test, y_test_repository)
        self.mape = mean_absolute_percentage_error(
            self.y_test, np.round(y_test_repository, 2))


    def model_post_init(self, __context):
        # Validate model
        if self.model is None:
            raise TypeError("You need to provide a model.")
        else:
            self.get_metrics()
        # Validate data_year
        if self.data_year > datetime.now().year:
            raise ValueError("data_year must not exceed the current year.")
        
        features = self.x_test.columns.to_list()
        # Validate inputs
        for input in self.inputs:
            if input.type == 'map':
                if input.lat not in features or input.lng not in features:
                    raise ValueError(
                        f"{input.column_name} is not a x_test column")
            else:
                if input.column_name not in features:
                    raise ValueError(
                        f"{input.column_name} is not a x_test column")


    def _prepare_json(self, zip_id):
        json_model = self.model_dump(exclude={"model", "x_test", "y_test"})
        # Convert non-serializable attributes
        json_model['x_test'] = self.x_test.to_dict(orient='records')
        json_model['y_test'] = self.y_test.tolist()
        json_model['id'] = zip_id
        
        return json_model


    def generate_zip(self):
        """
        Generate a zip file for a model including a json with the metrics and 
        the model itself. It will be stored in the model_development folder. 
        Upload the file to the link provided in class' attribute "model_link".

        Returns:
            folder_path (str): path of the ziped folder.
        """

        zip_id = str(uuid.uuid4())
        json_model = self._prepare_json(zip_id)

        # Configure tempdir
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._save_model(f'{tmp_dir}/{MODEL_FOLDER_NAME}')

            file_path = f"{tmp_dir}/{MODEL_JSON_NAME}"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(json_model, f, ensure_ascii=False, indent=4)

            folder_path = f"{DEV_FOLDER_PATH}/{zip_id}"

            try:
                # Save the model as zip
                shutil.make_archive(
                    folder_path, 
                    "zip",
                    root_dir=tmp_dir)
                print(f"""
Your model has been saved in the {DEV_FOLDER_PATH} folder as {zip_id}.zip.
To complete your contribution, please follow these steps:

- Run the `test_my_model` method of your ModelLogInput instance.
- Test your model on the app by making a prediciton.
- Upload the zip file to the location you specified in the `model_link` parameter.
- Open an issue in the project repository by filling the model contribution template in https://github.com/marcuszucareli/house-price-app/issues/new?template=model_upload.md
"""
                )
                return folder_path
            except Exception as e:
                raise ValueError(f'Error saving the model:\n{e}')


    def test_my_model(self, model_path):
        """
        Test the ingestion process of a model and insert it to the dev 
        database. Use it to test the model in streamlit.

        Args:
            model (str): the path to the zip file of the model.
        """
        import os
        import shutil
        from pathlib import Path
        from mlflow_client.ingestion import make_ingestion

        storage_path = Path(os.getenv("STORAGE_PATH", "/tmp/storage"))
        ingestion_path = Path(os.getenv("INGESTION_PATH", "/tmp/ingestion"))

        # Handle directory deletion/creation
        def prepare_dir(path: Path):
            if path.exists():
                for item in path.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            else:
                path.mkdir(parents=True, exist_ok=True)

        # Reset db
        init_db()

        # Prepare folders
        prepare_dir(storage_path)
        prepare_dir(ingestion_path)

        model_path_obj = Path(model_path)

        # Copy file to ingestion folder
        dest_file = ingestion_path / model_path_obj.name
        shutil.copy2(model_path_obj, dest_file)

        make_ingestion()
