import os
import shutil
import zipfile
from tests.conftest import standard_uuid
from database.init_db import init_db


def ensure_dir(path: str, clean: bool = False) -> None:
    if os.path.exists(path):
        if clean:
            shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)


def ensure_dev_model(storage):
    zip_source_path = f'tests/data/{standard_uuid}.zip'
    zip_destination_path = f'{storage}/{standard_uuid}'
    
    ensure_dir(zip_destination_path, clean=True)

    with zipfile.ZipFile(zip_source_path, 'r') as zip:
            zip.extractall(zip_destination_path)


ingestion_path = f'./tmp/ingestion'
storage_path = f'./tmp/storage'
ensure_dir(ingestion_path)
ensure_dir(storage_path)

ENV = os.getenv('ENV')
DB_PATH = os.getenv('DB_PATH')

if ENV == 'dev':
     ensure_dev_model(storage_path)
     if not os.path.exists(DB_PATH):
        init_db()
