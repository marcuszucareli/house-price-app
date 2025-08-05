import pytest
import os
import json
import shutil
from mlflow_client.ingestion import *
from mlflow_client.config import MODEL_FOLDER_NAME, MODEL_JSON_NAME


def test_should_ingest_success(ingestion_flow_env):

    ingestion_path = ingestion_flow_env[0]
    os.makedirs(str(ingestion_path / 'not_int_db'))
    from mlflow_client.ingestion import should_ingest
    
    should_ingest()


def test_should_ingest_fail_no_file(ingestion_flow_env):
    with pytest.raises(ValueError,
                       match='The ingestion folder is empty'):
        
        from mlflow_client.ingestion import should_ingest

        should_ingest()


def test_should_ingest_fail_many_files(ingestion_flow_env):
    with pytest.raises(ValueError,
                       match='The ingestion folder has more than 1 file.'):
        
        ingestion_path = ingestion_flow_env[0]

        not_in_db_1 = str(ingestion_path / 'not_in_db_1')
        not_in_db_2 = str(ingestion_path / 'not_in_db_2')

        os.makedirs(not_in_db_1)
        os.makedirs(not_in_db_2)

        from mlflow_client.ingestion import should_ingest
        
        should_ingest()


def test_should_ingest_fail_in_db(ingestion_flow_env):
    with pytest.raises(ValueError,
                       match='Model A already registered.'):
        
        from mlflow_client.ingestion import should_ingest

        ingestion_path = ingestion_flow_env[0]

        registered_model_path = str(ingestion_path / 'A')

        os.makedirs(registered_model_path)
        
        should_ingest()


def test_prepare_sql_values_success(ingestion_flow_env):

    std_json = ingestion_flow_env[4]

    model_table_values_true = model_table_values = (
        std_json['id'],
        std_json['flavor'],
        std_json['r2'],
        std_json['mae'],
        std_json['mape'],
        std_json['rmse'],
        std_json['algorithm'],
        std_json['data_year'],
        std_json['author'],
        json.dumps(std_json['links']),
    )
    
    city_table_values_true = []
    for city in std_json['cities']:
        city_table_values_true.append(
            (None, city, std_json['id'], std_json['country'])
        )
    
    inputs_table_values_true = []
    for input_ in std_json['inputs']:
        inputs_table_values_true.append(
            (
                None,
                std_json['id'],
                input_['column_name'],
                input_['lat'],
                input_['lng'],
                input_['label'],
                input_['type'],
                json.dumps(input_['options'], ensure_ascii=False),
                input_['description'],
                input_['unit']
            )
        )

    model_table_values, city_table_values, inputs_table_values = \
            prepare_sql_values(std_json)
    
    assert model_table_values_true == model_table_values
    assert city_table_values_true == city_table_values
    assert inputs_table_values_true == inputs_table_values


def test_sql_ingestion_success(ingestion_flow_env):
    
    ingestion_path = str(ingestion_flow_env[0])
    storage_path = str(ingestion_flow_env[1])
    standard_uuid = str(ingestion_flow_env[5])
    std_json = ingestion_flow_env[4]
    
    zip_source_path = f'tests/mlflow_client/data/{standard_uuid}.zip'
    zip_destination_path = f'{ingestion_path}/{standard_uuid}.zip'
    shutil.copy(zip_source_path, zip_destination_path)

    from database.init_db import init_db
    from mlflow_client.ingestion import make_ingestion

    init_db()

    make_ingestion()

    with get_connection() as conn:
        c =  conn.cursor()
        c.execute('SELECT * FROM models WHERE id=?',
                  (standard_uuid,))
        query_models = c.fetchall()

        c.execute('SELECT * FROM cities WHERE models_id=?',
                  (standard_uuid,))
        query_cities = c.fetchall()

        c.execute('SELECT * FROM inputs WHERE models_id=?',
                  (standard_uuid,))
        query_inputs = c.fetchall()

    # Check database registers
    assert len(query_models) == 1
    assert len(query_cities) == len(std_json['cities'])
    assert len(query_inputs) == len(std_json['inputs'])

    # Check storage file
    assert os.path.exists(f'{storage_path}/{standard_uuid}')
    
    assert os.path.exists(f'{ingestion_flow_env[1]}/{standard_uuid}/' \
                          f'{MODEL_FOLDER_NAME}')
    
    assert os.path.exists(f'{ingestion_flow_env[1]}/{standard_uuid}/' \
                          f'{MODEL_JSON_NAME}')