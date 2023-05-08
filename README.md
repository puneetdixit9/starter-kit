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
