import os
import shutil
import zipfile
import json
from tempfile import TemporaryDirectory
from database.connection import get_connection
from mlflow_client.config import MODEL_JSON_NAME


def should_ingest():
    INGESTION_PATH = os.getenv('INGESTION_PATH')

    # Check uniqueness of the file in file path
    files = os.listdir(INGESTION_PATH)

    if len(files) > 1:
        raise ValueError("The ingestion folder has more than 1 file.")

    if len(files) == 0:
        raise ValueError("The ingestion folder is empty.")
    
    file_name = files[0]
    file_path = f'{INGESTION_PATH}/{files[0]}'

    # Check if model is already registered
    model_id = os.path.splitext(file_name)[0]
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM models where id = ?", (model_id,))
        is_registered = c.fetchone()
    if is_registered:
        raise ValueError(f"Model {model_id} already registered.")
    
    return file_path, model_id


def prepare_sql_values(model_metadata):
    # Define model's table values
    model_table_values = (
        model_metadata['id'],
        model_metadata['flavor'],
        model_metadata['r2'],
        model_metadata['mae'],
        model_metadata['mape'],
        model_metadata['rmse'],
        model_metadata['algorithm'],
        model_metadata['data_year'],
        model_metadata['author'],
        json.dumps(model_metadata['links']),
    )

    # Define cities's table values
    cities = model_metadata['cities']
    city_table_values = []
    model_city_values = []
    for city in cities:
        city_value = (
            city['wikidata_id'],
            city['name'],
            city['country'],
            city['hierarchy'],
        )
        model_city_value = (
            None,
            city['wikidata_id'],
            model_metadata['id']
        )
        city_table_values.append(city_value)
        model_city_values.append(model_city_value)

    # Define inputs' table values
    inputs_table_values = []
    inputs = model_metadata['inputs']
    
    for model_input in inputs:
        input_value = (
            None,   # Autoincrement ID
            model_metadata['id'],
            model_input['column_name'],
            model_input['lat'],
            model_input['lng'],
            model_input['label'],
            model_input['type'],
            json.dumps(model_input['options'], ensure_ascii=False),
            model_input['description'],
            model_input['unit']
        )
        inputs_table_values.append(input_value)

    return model_table_values, city_table_values, model_city_values,\
        inputs_table_values


def make_ingestion():
    STORAGE_PATH = os.getenv('STORAGE_PATH')

    file_path, model_id = should_ingest()
    # Unzip file
    with TemporaryDirectory() as tmp:
        extraction_path =f'{tmp}/{model_id}'
        # Create file folder
        os.makedirs(extraction_path)
        with zipfile.ZipFile(file_path, 'r') as zip:
            zip.extractall(extraction_path)
        
        # Prepare metadata
        with open(
            f'{extraction_path}/{MODEL_JSON_NAME}', 'r', encoding='utf-8') \
            as f:
            model_metadata = json.load(f)

        model_table_values, city_table_values, \
        model_city_values, inputs_table_values = \
            prepare_sql_values(model_metadata)

        # Insert data in database and save the model in the production folder
        with get_connection() as conn:
            try:
                c = conn.cursor()
                
                # Begin transactiion
                c.execute("BEGIN")
                # Insert model
                c.execute(
                    "INSERT INTO models VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    model_table_values
                )
                # Insert city
                for city in city_table_values:
                    c.execute(
                        "INSERT OR IGNORE INTO cities VALUES (?, ?, ?, ?)",
                        city
                    )
                # Insert city model relation
                for relation in model_city_values:
                    c.execute(
                        "INSERT INTO model_city VALUES (?, ?, ?)",
                        relation
                    )
                # Insert inputs
                for model_input in inputs_table_values:
                    c.execute(
                        "INSERT INTO inputs VALUES" \
                        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        model_input
                    )
                
                # Move model folder to storage
                shutil.move(extraction_path, STORAGE_PATH)

                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
