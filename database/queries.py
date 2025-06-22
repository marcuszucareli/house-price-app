country = """
SELECT DISTINCT country
FROM models
ORDER BY country
"""
cities = """
SELECT DISTINCT city
FROM cities
WHERE country=:country
ORDER BY city
"""
models_of_city = """
SELECT *
FROM models
WHERE id IN (
    SELECT models_id
    FROM cities
    WHERE city=:city
)
ORDER BY {sort}
"""