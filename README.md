# Starter Kit using Python in Flask framework

## Server Setup
* Install Python 3.10
* Create and activate Virtual Environment
* Install requirements
```commandline
pip install -r requirements.txt
```
* Migrate Database
```commandline
flask db init
flask db migrate
flask db upgrade
```
* Run Server
```commandline
flask run
```

## Pre-Commit Hooks Setup
* Install Pre-commit hooks
```commandline
pre-commit install
```
* Run Pre-commit hooks. (Pre-commit hooks will run only on Staged Changes).
No need to run any command manually. It will auto run on git commit command.
But you can try to run it using the below command.
```commandline
pre-commit run
```


## Unit testing
1. Auth routers unit testing
```commandline
(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.auth_router_tests.AuthRouterTest
........
----------------------------------------------------------------------
Ran 8 tests in 1.349s

OK
```
2. Main routers unit testing

```commandline
(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.main_router_tests.MainRouterTest
......
----------------------------------------------------------------------
Ran 6 tests in 1.173s

OK
```
3. Database Models unit testing
```commandline

(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.models_tests.ModelsTests
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```
