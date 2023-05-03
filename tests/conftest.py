# Define fixture her to make a fixture available to multiple test files

# import uuid
# from json import loads

from pytest import fixture

from main import get_app
from main.db import db
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser

# --------
# Fixtures
# --------


@fixture(scope="class")
def test_user():
    created_id = AuthUserController.create_new_user(
        {"username": "testuser", "email": "testadmin@gmail.com", "password": "test_password", "role": "user"}
    )
    user = AuthUser.query.filter_by(id=created_id).first()
    return user


@fixture(scope="session", autouse=True)
def test_client():
    # Create a Flask app configured for testing
    flask_app = get_app(env="test")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@fixture(scope="module")
def init_database():
    db.create_all()


# @fixture(scope="class")
# def import_users():
#     """
#     Create new users data from data/users.json
#     """
#     with open("tests/data/users.json", "r") as user_file:
#         users = loads(user_file.read())

#     # Create the database and the database table
#     db.create_all(bind_key="user")

#     # store users in Users table

#     for user in users:
#         db.session.add(Users(**user, public_id=str(uuid.uuid4())))
#     db.session.commit()
