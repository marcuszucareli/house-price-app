-- models table
INSERT INTO models VALUES (
    "A",
    "sklearn",
    .1962,
    1963,
    .2002,
    .2004,
    "Random forest",
    2011,
    "Giovanni Silva de Oliveira",
    '{"linkedin": "www.linkedin.com", "github": "www.github.com"}'
);

INSERT INTO models VALUES (
    "B",
    "xgboosting",
    .7,
    2000,
    .18,
    .2004,
    "xgboosting",
    2025,
    "Edson Arantes do Nascimento",
    '{"linkedin": "www.linkedin.com", "github": "www.github.com"}'
);

INSERT INTO models VALUES (
    "C",
    "sklearn",
    .8,
    1987,
    .09,
    .2025,
    "Regression",
    2015,
    "Neymar Jr",
    '{"linkedin": "www.linkedin.com", "github": "www.github.com"}'
);

-- cities table
INSERT INTO cities VALUES (
    NULL,
    "São José dos Campos",
    "A",
    "Brazil"
);

INSERT INTO cities VALUES (
    NULL,
    "Jacareí",
    "A",
    "Brazil"
);

INSERT INTO cities VALUES (
    NULL,
    "Taubaté",
    "A",
    "Brazil"
);

INSERT INTO cities VALUES (
    NULL,
    "Belo Horizonte",
    "A",
    "Brazil"
);

INSERT INTO cities VALUES (
    NULL,
    "Belo Horizonte",
    "B",
    "Brazil"
);

INSERT INTO cities VALUES (
    NULL,
    "Paris",
    "C",
    "France"
);

INSERT INTO cities VALUES (
    NULL,
    "Dijon",
    "C",
    "France"
);

-- inputs table
INSERT INTO inputs VALUES (
    NULL,
    'A',
    'n_bedrooms',
    'Bedroom',
    'int',
    '[]',
    'Number of bedrooms',
    ''
);

INSERT INTO inputs VALUES (
    NULL,
    'A',
    'is_new',
    'New',
    'bool',
    '[]',
    'Under 5 years old',
    'years'
);

INSERT INTO inputs VALUES (
    NULL,
    'A',
    'area',
    'Area',
    'float',
    '[]',
    'The area in m²',
    'm²'
);

INSERT INTO inputs VALUES (
    NULL,
    'A',
    'neighbourhood',
    'Neighbourhood',
    'categorical',
    '["block 1", "block 2", "block 3"]',
    'The area in m²',
    'm²'
);

INSERT INTO inputs VALUES (
    NULL,
    'A',
    'map',
    'map',
    'map',
    '[]',
    'Coordinates',
    ''
);