import pandas as pd
import numpy as np
import mlflow.pyfunc
import tempfile
from pydantic import BaseModel
from dataclasses import field
from typing import Optional, Any
from datetime import datetime
from sklearn.metrics import  r2_score, root_mean_squared_error, \
    mean_absolute_percentage_error, mean_absolute_error

# Define the maximum number of chars in strings
max_chars = 64


class Inputs(BaseModel):
    """
    Defines the necessary parameters that each input of the model should have.

    Args:
        column_name (str): The column name in the model.
        label (str): The name to be displayed in the Streamlit app.
        type (str): The type of the input. Must be one of the following
                    options:
            - "bool":  A boolean parameter.
            - "int": An int parameter.
            - "float": An float parameter.
            - "categorical": A categorical parameter. If choosing "categorical"
                you must specify the options attribute.
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
    label: str
    type: str
    options: Optional[list[str]] = field(default_factory=list)
    description: Optional[str] = ''
    unit: Optional[str] = ''


    def model_post_init(self, __context):
        allowed_data_types = ['bool', 'int', 'float', 'categorical']
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
        
        if isinstance(self.description, str) and \
            len(self.description) > 200:
            
            raise ValueError("label cannot be longer than 128 characters")
        
        if isinstance(self.unit, str) and \
            len(self.unit) > max_chars:
            raise ValueError("label cannot be longer than 128 characters")


class ModelLogInput(BaseModel):
    """
    Validates model information to ensure compliance with the project's logging
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
        country (str): The country associated with the data. Must follow the 
        ISO 3166 country name standard.
        See: https://www.iso.org/iso-3166-country-codes.html
        cities (list[str]): A list of cities associated with the data.
        inputs (list[Inputs]): A list of user-provided inputs required to make 
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
    country: str
    cities: list[str]
    inputs: list[Inputs]
    author: Optional[str] = None
    links: Optional[dict[str, str]] = {}


    def temp_save_model(self, tmp_dir):
        registered_model_name = 'test_model'
        match self.flavor:
                case "sklearn":
                    import mlflow.sklearn
                    mlflow.set_tracking_uri(f"file:{tmp_dir}")
                    mlflow.sklearn.save_model(
                        sk_model=self.model,
                        path=tmp_dir
                    )

                case "xgboost":
                    import mlflow.xgboost
                    mlflow.set_tracking_uri(f"file:{tmp_dir}")
                    mlflow.xgboost.save_model(
                        xgb_model=self.model,
                        registered_model_name=registered_model_name,
                        path=tmp_dir
                    )

                case "lightgbm":
                    import mlflow.lightgbm
                    mlflow.set_tracking_uri(f"file:{tmp_dir}")
                    mlflow.lightgbm.save_model(
                        lgbm_model=self.model,
                        registered_model_name=registered_model_name,
                        path=tmp_dir
                    )

                case "catboost":
                    import mlflow.catboost
                    mlflow.set_tracking_uri(f"file:{tmp_dir}")
                    mlflow.catboost.save_model(
                        model=self.model,
                        registered_model_name=registered_model_name,
                        path=tmp_dir
                    )

                case "keras" | "tensorflow":
                    import mlflow.keras
                    mlflow.set_tracking_uri(f"file:{tmp_dir}")
                    mlflow.keras.save_model(
                        keras_model=self.model,
                        registered_model_name=registered_model_name,
                        path=tmp_dir
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
            # Save the model
            self.temp_save_model(tmp_dir)
            
            # Load model using pyfunc
            model_loaded = mlflow.pyfunc.load_model(tmp_dir)

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
        # Validate inputs
        for input in self.inputs:
            if input.column_name not in self.x_test.columns.to_list():
                raise ValueError(f"{input.column_name} is not a x_test column")
