INSERT INTO models VALUES (
'00000000-0000-0000-0000-000000000000',
'sklearn',
0.99,
99,
0.99,
0.99,
'regression',
1999,
'Edson Arantes do Nascimento',
'{"Github": "https://github.com/", "Linkedin": "https://www.linkedin.com/"}'
);
INSERT INTO cities VALUES (
'Q42800',
'Belo Horizonte',
'Brazil',
'Minas Gerais'
);
INSERT INTO model_city VALUES (
NULL,
'Q42800',
'00000000-0000-0000-0000-000000000000'
);
INSERT INTO cities VALUES (
'Q1439211',
'Três Corações',
'Brazil',
'Minas Gerais'
);
INSERT INTO model_city VALUES (
NULL,
'Q1439211',
'00000000-0000-0000-0000-000000000000'
);
INSERT INTO inputs VALUES (
NULL,
'00000000-0000-0000-0000-000000000000',
'neighbourhood',
'lat',
'lng',
'Neighbourhood',
'categorical',
'["Morumbi", "América"]',
"Property neighbourhood",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'00000000-0000-0000-0000-000000000000',
'is_new',
'lat',
'lng',
'Is your house new?',
'bool',
'[]',
"If your house has less than 5 years",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'00000000-0000-0000-0000-000000000000',
'n_bedrooms',
'lat',
'lng',
'Number of bedrooms in the house',
'int',
'[]',
NULL,
'un'
);
INSERT INTO inputs VALUES (
NULL,
'00000000-0000-0000-0000-000000000000',
'area_m2',
'lat',
'lng',
'Area',
'float',
'[]',
"The property size in m².",
'm²'
);
INSERT INTO inputs VALUES (
NULL,
'00000000-0000-0000-0000-000000000000',
'map',
'latitude',
'longitude',
'Coordinates',
'map',
'[]',
"house's Latitude and Longiude",
NULL
);
INSERT INTO models VALUES (
'11111111-1111-1111-1111-111111111111',
'sklearn',
0.98,
98,
0.98,
0.98,
'gradient boosting',
1998,
'Douglas Adams',
'{"Github": "https://github.com/"}'
);
INSERT INTO cities VALUES (
'Q350',
'Cambridge',
'United Kingdom',
'Cambridge'
);
INSERT INTO model_city VALUES (
NULL,
'Q350',
'11111111-1111-1111-1111-111111111111'
);
INSERT INTO inputs VALUES (
NULL,
'11111111-1111-1111-1111-111111111111',
'is_new',
'lat',
'lng',
'Is your house new?',
'bool',
'[]',
"If your house has less than 5 years",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'11111111-1111-1111-1111-111111111111',
'n_bedrooms',
'lat',
'lng',
'Number of bedrooms in the house',
'int',
'[]',
NULL,
'un'
);
INSERT INTO inputs VALUES (
NULL,
'11111111-1111-1111-1111-111111111111',
'area_m2',
'lat',
'lng',
'Area',
'float',
'[]',
"The property size in m².",
'm²'
);
INSERT INTO inputs VALUES (
NULL,
'11111111-1111-1111-1111-111111111111',
'map',
'latitude',
'longitude',
'Coordinates',
'map',
'[]',
"house's Latitude and Longiude",
NULL
);
INSERT INTO models VALUES (
'22222222-2222-2222-2222-222222222222',
'sklearn',
0.97,
97,
0.97,
0.97,
'random forest',
1997,
'Aurora Aksnes',
'{"Linkedin": "https://www.linkedin.com/"}'
);
INSERT INTO cities VALUES (
'Q585',
'Oslo',
'Norway',
'Oslo Municipality'
);
INSERT INTO model_city VALUES (
NULL,
'Q585',
'22222222-2222-2222-2222-222222222222'
);
INSERT INTO cities VALUES (
'Q26793',
'Bergen',
'Norway',
'Bergen Municipality'
);
INSERT INTO model_city VALUES (
NULL,
'Q26793',
'22222222-2222-2222-2222-222222222222'
);
INSERT INTO inputs VALUES (
NULL,
'22222222-2222-2222-2222-222222222222',
'is_new',
'lat',
'lng',
'Is your house new?',
'bool',
'[]',
"If your house has less than 5 years",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'22222222-2222-2222-2222-222222222222',
'n_bedrooms',
'lat',
'lng',
'Number of bedrooms in the house',
'int',
'[]',
NULL,
'un'
);
INSERT INTO inputs VALUES (
NULL,
'22222222-2222-2222-2222-222222222222',
'area_m2',
'lat',
'lng',
'Area',
'float',
'[]',
"The property size in m².",
'm²'
);
