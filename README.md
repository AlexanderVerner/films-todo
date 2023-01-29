# Films TODO

## Run Tests Locally
```sh
# Run all the tests for all the apps
docker-compose exec web ./run_tests_locally.py
# Run tests for an app
docker-compose exec web ./run_tests_locally.py todo
# Run tests from a given module (a file)
docker-compose exec web ./run_tests_locally.py todo.tests.test_view
# Run a single test case
docker-compose exec web ./run_tests_locally.py todo.tests.test_view.IndexViewTests
# Run a single test
docker-compose exec web ./run_tests_locally.py todo.tests.test_view.IndexViewTests.test_get_index_view
```

## Run Tests in PyCharm
To start tests in PyCharm you need to set custom settings `_project_/run_tests_settings.py`
