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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
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
'',
'',
'Area',
'float',
'[]',
"The property size in m².",
'm²'
);
INSERT INTO models VALUES (
'55555555-5555-5555-5555-555555555555',
'sklearn',
0.96,
96,
0.96,
0.96,
'random forest',
2024,
'Marcus Zucareli',
'{"Linkedin": "https://www.linkedin.com/"}'
);
INSERT INTO cities VALUES (
'Q191642',
'São José dos Campos',
'Brazil',
'São Paulo'
);
INSERT INTO model_city VALUES (
NULL,
'Q191642',
'55555555-5555-5555-5555-555555555555'
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'rooms',
'',
'',
'Quartos',
'int',
'[]',
"Número de quartos do imóvel.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'parking',
'',
'',
'Vagas',
'int',
'[]',
"Número de vagas do imóvel.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'bathrooms',
'',
'',
'Banheiros',
'int',
'[]',
"Número de banheiros do imóvel.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'area',
'',
'',
'Área',
'float',
'[]',
"Tamanho do imóvel.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'has_multiple_parking_spaces',
'',
'',
'Múltiplas vagas de garagem.',
'bool',
'[]',
"Se o seu imóvel possui mais de uma vaga de garagem.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'neighbourhood',
'',
'',
'Bairro',
'categorical',
'["Jardim Esplanada", "Conjunto Residencial Trinta e Um de Março", "Vila Betânia", "Parque Residencial Aquarius", "Floradas de São José", "Jardim São Dimas", "Parque Industrial", "Centro", "Vila Adyana", "Jardim Augusta", "Jardim América", "Vila Alexandrina", "Jardim Oswaldo Cruz", "Jardim Bela Vista", "Jardim Satélite", "Vila Ema", "Urbanova VI", "Jardim Fátima", "Jardim Santa Madalena", "Jardim das Colinas", "Vila Iracema", "Monte Castelo", "Jardim Sul", "Palmeiras de São José", "Vila Sanches", "Jardim Apolo I", "Jardim das Indústrias", "Parque Residencial Flamboyant", "Cidade Morumbi", "Condomínio Residencial Colinas do Paratehy", "Jardim Apolo II", "Jardim Esplanada II", "Vila Industrial", "Altos do Esplanada", "Chácaras São José", "Jardim Paraíso", "Loteamento Terra Brasilis", "Loteamento Urbanova II", "Jardim Topázio", "Condomínio Royal Park", "Jardim Americano", "Jardim Vale do Sol", "Bosque dos Eucaliptos", "Jardim Alvorada", "Jardim Aparecida", "Jardim Veneza", "Jardim Terras do Sul", "Residencial Frei Galvão", "Jardim Portugal", "Urbanova", "Jardim Oriente", "Jardim San Marino", "Jardim Uirá", "Jardim Souto", "Vila São Benedito", "Jardim Paraíso do Sol", "Vila Maria", "Cidade Vista Verde", "Vila Rangel", "Jardim Estoril", "Vila Tatetuba", "Loteamento Floresta", "Jardim Petrópolis", "Jardim Ismênia", "Jardim Nova América", "Jardim Maritéia", "Jardim Minas Gerais", "Residencial Bosque dos Ipês", "Jardim Rodolfo", "Jardim Aquárius", "Jardim Torrão de Ouro", "Bom Retiro", "Jardim Nova Michigan", "Vila Cardoso", "Jardim São Judas Tadeu", "Vila Rubi", "Parque Nova Esperança", "Jardim dos Bandeirantes", "Loteamento Residencial Vista Linda", "Jardim São José II", "Jardim Anhembi", "Jardim Copacabana", "Outros"]',
"Bairro do seu imóvel.",
NULL
);
INSERT INTO inputs VALUES (
NULL,
'55555555-5555-5555-5555-555555555555',
'',
'lat_value',
'lon_value',
'Coordenadas',
'map',
'[]',
NULL,
NULL
);
