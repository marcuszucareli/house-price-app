CREATE TABLE IF NOT EXISTS models (
    id TEXT PRIMARY KEY,
    flavor TEXT,
    r2 REAL,
    mae REAL,
    mape REAL,
    rmse REAL,
    algorithm TEXT,
    data_year INTEGER,
    author TEXT,
    links TEXT
);

CREATE TABLE IF NOT EXISTS cities (
    id TEXT PRIMARY KEY,
    city TEXT,
    country TEXT,
    hierarchy TEXT
);

CREATE TABLE IF NOT EXISTS model_city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cities_id TEXT,
    models_id TEXT,
    FOREIGN KEY(cities_id) REFERENCES cities(id),
    FOREIGN KEY(models_id) REFERENCES models(id)
);

CREATE TABLE IF NOT EXISTS inputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    models_id TEXT,
    column_name TEXT,
    lat TEXT,
    lng TEXT,
    label TEXT,
    type TEXT,
    options TEXT,
    description TEXT,
    unit TEXT,
    FOREIGN KEY(models_id) REFERENCES models(id)
);