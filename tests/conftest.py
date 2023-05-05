import json
import os

import pytest

from main import get_app
from main.db import db


@pytest.fixture(scope="class")
def app():
    """
    This is the fixture function for create the instance of app and to create all the db tables.
    On teardown, it drops the tables.
    :return:
    """
    app = get_app("test")
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="class")
def client(app):
    """
    This fixture function is used to create a test client of the app to execute the tests.
    :param app:
    :return:
    """
    return app.test_client()


@pytest.fixture(scope="class")
def load_data_from_file(app):
    def _load_data(model, filepath):
        """
        This fixture function is used to read the data from a file and add that data into given model.
        Model can be anything, you just have to pass a valid json file path for that model.
        :param model:
        :param filepath:
        :return:
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        with app.app_context():
            with open(os.path.join(basedir, filepath)) as f:
                data = json.load(f)
                for item in data:
                    model_instance = model(**item)
                    db.session.add(model_instance)
                db.session.commit()

    return _load_data


@pytest.fixture(scope="class")
def load_data_to_model_using_controller_from_file(app):
    def _load_data(controller_function, filepath):
        """
        This fixture function is used to read the data from a file and add that data into its table
        through its controller function. you just have to pass a valid json file path and controller
        function
        :param controller_function: A function which is used to create record to a particular table.
        :param filepath:
        :return:
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        with app.app_context():
            with open(os.path.join(basedir, filepath)) as f:
                data = json.load(f)
                for item in data:
                    controller_function(item)

    return _load_data
