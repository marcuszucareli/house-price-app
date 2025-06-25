queries = {
    'get_all_countries': """
SELECT DISTINCT country
FROM models
ORDER BY country
""",

    'get_all_cities': """
SELECT DISTINCT city
FROM cities
WHERE (:country IS NULL OR country = :country)
ORDER BY city
""",

    'get_models_from_city': """
SELECT *
FROM models
WHERE id IN (
    SELECT models_id
    FROM cities
    WHERE (:city IS NULL OR city = :city)
)
ORDER BY {sort_by}
""",

    'test_fetch_query': """
SELECT id FROM models WHERE 1 = ?
""",

    'test_execute_query_insert': """
INSERT INTO cities VALUES (
    NULL,
    "Paris",
    "D",
    "France"
)
""",

    'test_execute_query_get': """
SELECT city FROM cities WHERE models_id = "D"
"""
}