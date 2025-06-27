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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    models_id TEXT,
    country TEXT,
    FOREIGN KEY(models_id) REFERENCES models(id),
    FOREIGN KEY(country) REFERENCES models(country)
);

CREATE TABLE IF NOT EXISTS inputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    models_id TEXT,
    column_name TEXT,
    label TEXT,
    type TEXT,
    options TEXT,
    description TEXT,
    unit TEXT,
    FOREIGN KEY(models_id) REFERENCES models(id)
);