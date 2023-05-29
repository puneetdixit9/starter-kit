# Starter Kit using Python in Flask framework

## Server Setup
* Install Python 3.10
* Go to the root directory of your project and run these commands to create and activate Virtual Environment
```commandline
$ python3 -m venv env
$ source env/bin/activate
```
* Install requirements
```commandline
$ pip install -r requirements.txt
```
* Create a file at **_/root_** path or your project with name **_.env_** and with below data.
```doctest
DATABASE_URL=mysql+mysqlconnector://<DB_USERNAME>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
TESTING_DATABASE_URL=mysql+mysqlconnector://<TEST_DB_USERNAME>:<TEST_DB_PASSWORD>@<TEST_DB_HOST>:<TEST_DB_PORT>/<TEST_DB_NAME>
SECRET_KEY=<YOUR SECRET KEY>
CACHE_REDIS_HOST=<REDIS_HOST>
CACHE_REDIS_PORT=<REDIS_PORT>
CACHE_REDIS_DB=<REDIS_DB>
```
* Migrate Database
```commandline
$ flask db init
$ flask db migrate -m "migration message"
$ flask db upgrade
```
If facing error like **Error: Target database is not up-to-date.**
in **flask db migrate** command then run these commands.
```commandline
$ flask db stamp head
$ flask db migrate -m "migration message"
$ flask db upgrade
```
* Upgrade or Downgrade and particular migration version
```commandline
$ flask db upgrade 'migration_version'
 ```
```commandline
$ flask db downgrade 'migration_version'
```
* Run Server
```commandline
$ flask run
```

## Tests
Pytest (python package) is being used in the tests. All test files
should be in the tests directory and file name should start with test_


For Example

```doctest
test_module.py
```
And all test function should also start with test_

For Example.
```doctest
def test_get_records():
    records = Records.get_all()
    assert len(records) == 2
```
We have two types of tests in this starter kit.
* Integration tests (To test the APIs)
* Unit tests (To test each an every function)

You can run the tests with the following commands.
* Run all tests.
```commandline
$ pytest
```
* Run tests in a directory
```commandline
$ pytest tests/
```
* Run a specific file.
```commandline
$ pytest tests/filename.py
```
* Run a test a specific file
```commandline
$ pytest tests/filename.py::test_method
```
* Run a test class from a specific file
```commandline
$ pytest tests/filename.py::TestClass
```
* Run a test of a test class from a specific file
```commandline
$ pytest tests/filename.py::TestClass::test_method
```
Output of pytest:
```doctest
$ pytest
=============================================================== 73 passed in 22.36s ===============================================================
```
## Code Coverage by tests
To check the code coverage by tests we are using
coverage package. We can check the coverage (how
much tests is covered by unit and integration tests)
by tests of each directory.

You can check the coverage of unit tests and integration_tests separately

Command to run the coverage.
```commandline
$ coverage run --source=main -m pytest -v ./tests ; coverage report -m
```
Output of coverage:
```doctest
$ coverage run --source=main -m pytest -v ./tests ; coverage report -m

=============================================================== 73 passed in 23.32s ===============================================================
Name                                           Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------
main\__init__.py                                  28      0   100%
main\custom_exceptions\__init__.py                 3      0   100%
main\custom_exceptions\exception_handlers.py      17      0   100%
main\custom_exceptions\exceptions.py              12      0   100%
main\db\__init__.py                               24      0   100%
main\logging_module\__init__.py                    4      0   100%
main\logging_module\logger.py                     19      0   100%
main\modules\__init__.py                          12      0   100%
main\modules\address\controller.py                38      0   100%
main\modules\address\model.py                     14      0   100%
main\modules\address\schema_validator.py          14      0   100%
main\modules\address\view.py                      39      0   100%
main\modules\auth\controller.py                   51      0   100%
main\modules\auth\model.py                        13      0   100%
main\modules\auth\schema_validator.py             20      0   100%
main\modules\auth\view.py                         42      0   100%
main\modules\jwt\controller.py                    27      0   100%
main\modules\jwt\model.py                          6      0   100%
main\modules\user\controller.py                   19      0   100%
main\modules\user\model.py                         9      0   100%
main\modules\user\schema_validator.py              7      0   100%
main\modules\user\view.py                         31      0   100%
main\utils.py                                     91      0   100%
----------------------------------------------------------------------------
TOTAL                                            540      0   100%
```

## Pre-Commit Hooks Setup
* Install Pre-commit hooks
```commandline
$ pre-commit install
```
* Run Pre-commit hooks. (Pre-commit hooks will run only on Staged Changes).
No need to run any command manually. It will auto run on git commit command.
But you can try to run it using the below command.
```commandline
$ pre-commit run
```
Output:
```commandline
$ pre-commit run

Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Isort (python)...........................................................Passed
Black....................................................................Passed
Flake8...................................................................Passed
Unit tests and code coverage.............................................Passed
Integration tests and code coverage......................................Passed
```

* You can skip pre-commit auto run on git commit using this flag --no-verify flag
```commandline
$ git commit -m "YOUR COMMIT MESSAGE" --no-verify
```
