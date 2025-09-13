# Tests
Tests are divided into folders named after projects' modules, with a common conftest file defining the dev database and standard inputs. We use Pytest to write and run unit tests. They are also divided by file, so each file in every module of the project has a corresponding test file with the same name.

## About the dev database
All the information about the dev database is listed in the [database file](./database.md#dev-database).

## Specific tests scenarios
Based on the different records in our dev database, some tests require us to pick the right model to be properly run.

1. **Testing predict endpoint**

As listed in the [dev database description](./database.md#dev-database), the only record associated with a true existing model is the one with uuid of 5's*. For this reason, the prediction endpoint must use it to be tested, otherwise the test will fail. Its inputs are listed bellow.

>⚠️ * Every test you need to write that involves predicting must used the 5's UUID. 

| Name                         | Type   | Description                                                   |
|------------------------------|--------|---------------------------------------------------------------|
| neighbourhood                | str    | A categorical variable representing the location of the property |
| area                         | float  | The area of the property                                      |
| rooms                        | int    | The number of rooms in the property                           |
| parking                      | int    | The number of parking spaces available                        |
| bathrooms                    | int    | The number of bathrooms in the property                       |
| price                        | float  | The property's price                                          |
| lat_value                    | float  | The latitude of the property's street                         |
| lon_value                    | float  | The longitude of the property's street                        |
| has_multiple_parking_spaces  | bool   | Indicates if the property has at least 2 parking spaces       |

2. **Testing the results page**

In order to reach results page you'll need to run a predict consult, that means you'll have to pick the same model described above to test/visualize it. Mocking this API response to avoid this counterproductive step is on our To-Do list.

## API
API's conftest file has a client fixture that already setup the test client and the storage with the standar model.

## mlflow_client conftest
mlflow_client conftest file has a fixture to generate a ModelLogInput instance and also one to mimic the ingestion environment.

## Running tests
The proccess to run tests is described in our [code contribution guide](./contributing/code.md).