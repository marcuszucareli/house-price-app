#  😃 Welcome!

Thanks for contributing to the project! If you’re here, it means you’ve already [set up your development environment](../../README.md#getting-started-locally). This document outlines the process to collaborate with translations.

## Project Standards

Before starting the translation, we suggest you to take a look into these chapters of the code contribution file:

- [🔀 Pull requests](./code.md#🔀-pull-requests)
- [🌿 Branching Model](./code.md#🌿-branching-model)
- [🧑‍💻 Commit Messages](./code.md#🧑‍💻-commit-messages)
- [✅ Tests](./code.md#✅-tests)

## Translating

We only keep [this file](../../app/translations.py) for storing translations. The file has 3 dictionaries stored in 3 variables:

in `available_languages` insert your language's name in your idiom as key, and its corresponding abreviation as value.

`main` and `results` are the pages of our web application. For each item in their dictionaries, you'll add your language's abreviation as the key, and te translation as the value.

Make sure to keep identation, markdown anotations (`#`), markers (`:color[]`) and placeholders (`{value:,.0f}`)

example:

```python
# Before translation
{
    "error": {
        'en': """
# I'm {name} an i have :green[$ {value:,.0f}] in my bank account.

- uow!
"""
    }
}

# After translation to portuguese (pt)
{
    "error": {
        'en': """
# I'm {name} an i have :green[$ {value:,.0f}] in my bank account.

- uow!
"""
    },
        'pt': """
# Me chamo {name} e eu tenho :green[$ {value:,.0f}] na minha conta bancária.

- uow!
"""
}
```

After finishing the translations, make sure to test the app locally to see if it works. To test the results page, use the [standard predicting model](../database.md#dev-database) following this sequence in the app home:

1. Country: Brazil
2. City: São José dos Campos
3. Pick a random point on the map
4. Fill the form (Fields are `neighbourhood`, `area`, `bedrooms`, `parking spaces`, and `bathrooms`)
5. Click on the button at the bottom of the page