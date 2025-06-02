import pandas as pd
import numpy as np
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime

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
        description (Optional[str] = None): A brief description of the 
        parameter.
        unit (Optional[str] = None): Unit of measurement associated with the 
        parameter.
    """
    model_config = {
        "arbitrary_types_allowed": True
    }
    column_name: str
    label: str
    type: str
    options: Optional[list[str]] = field(default_factory=list)
    description: Optional[str] = None
    unit: Optional[str] = None


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
        mape (float | int): Mean Absolute Percentage Error of the model in 
        decimal form.
        mae (float | int): Mean Absolute Error of the model.
        rmse (float | int): Root Mean Squared Error of the model.
        r2 (float | int): R-squared of the model
        x_test (pd.DataFrame): A sample of 100 rows from the model's test
         data, used for validation and logging.
        y_predict (pd.Series | np.ndarray): The prediction associated with the
         x_test data, used for validation and logging..
        author (str): The author of the model
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
    """
    # Set pydantic configs
    model_config = {
        "arbitrary_types_allowed": True
    }

    # Model
    model: Any

    # Metrics
    mape: float | int
    mae: float | int
    rmse: float | int
    r2: float | int

    # Artefacts
    x_test: pd.DataFrame
    y_predict: pd.Series | np.ndarray

    # Tags
    author: str
    algorithm: str
    data_year: int
    country: str
    cities: list[str]
    inputs: list[Inputs]


    def model_post_init(self, __context):
        # Validate model
        if self.model is None:
            raise TypeError("You need to provide a model.")
        # Validate mape decimal form
        if self.mape < 0 or self.mape > 1:
            raise ValueError("MAPE must be provided in decimal form.")
        # Validate x_test
        if len(self.x_test) != 100:
            raise ValueError("x_test must have 100 lines")
        # Validate y_test
        if len(self.y_predict) != 100:
            raise ValueError("y_predict must have 100 lines")
        # Validate R²
        if self.r2 < -1 or self.r2 > 1:
            raise ValueError("R² value must be between -1 and 1.")
        # Validate data_year
        if self.data_year > datetime.now().year:
            raise ValueError("data_year must not exceed the current year.")
        # Validate inputs
        for input in self.inputs:
            if input.column_name not in self.x_test.columns.to_list():
                raise ValueError(f"{input.column_name} is not a x_test column")
