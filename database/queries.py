queries = {
    'get_all_countries': """
SELECT DISTINCT country
FROM cities
ORDER BY country
""",

    'get_all_cities': """
SELECT id, city
FROM cities
WHERE (:country IS NULL OR country = :country)
ORDER BY city
""",

    'get_models_from_city': """
SELECT *
FROM models
WHERE id IN (
    SELECT models_id
    FROM model_city
    WHERE (:city_id IS NULL OR cities_id = :city_id)
)
ORDER BY {sort_by}
""",

    'get_model': """
SELECT *
FROM models
WHERE id = :model_id
""",

    'get_inputs': """
SELECT *
FROM inputs
WHERE models_id = :model_id
ORDER BY type
""",

    'test_fetch_query': """
SELECT id FROM models WHERE 1 = ?
""",

    'test_execute_query_insert': """
INSERT INTO cities VALUES (
    "D",
    "Paris",
    "France",
    "Ile-de-France"
)
""",

    'test_execute_query_insert_many': """
INSERT INTO cities VALUES (
    ?,
    "Paris",
    "France",
    "Ile-de-France"
)
""",

    'test_execute_query_get': """
SELECT city FROM cities WHERE id = "D" OR id = "E"
"""
}