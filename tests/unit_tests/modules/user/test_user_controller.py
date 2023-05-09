import pytest
from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.modules.auth.model import AuthUser
from main.modules.user.controller import UserController

USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2


def get_header(user_id: int = USER_ROLE_ID):
    access_token = create_access_token(identity={"user_id": user_id})
    header = {"Authorization": f"Bearer {access_token}"}
    return header


@pytest.fixture(scope="function")
def add_fixtures(load_data_from_file):
    load_data_from_file(AuthUser, "unit_tests/fixtures/auth_users.json")


def test_get_user_profile(app, add_fixtures):
    with app.app_context():
        profile = UserController.get_profile(1)
        assert profile != {}
        with app.test_request_context(headers=get_header()):
            verify_jwt_in_request()
            profile = UserController.get_profile()
            assert profile != {}


def test_update_user_profile(app, add_fixtures):
    with app.app_context():
        profile = UserController.get_profile(2)
        assert profile["department"] is None
        UserController.update_user_profile({"department": "test123"}, 2)
        profile = UserController.get_profile(2)
        assert profile["department"] == "test123"
        with app.test_request_context(headers=get_header()):
            verify_jwt_in_request()
            profile = UserController.get_profile()
            assert profile["department"] is None
            UserController.update_user_profile({"department": "test123"})
            profile = UserController.get_profile()
            assert profile["department"] == "test123"


def test_get_users_profile(app, add_fixtures):
    with app.app_context():
        with app.test_request_context(headers=get_header(ADMIN_ROLE_ID)):
            verify_jwt_in_request()
            profiles = UserController.get_profiles()
            assert len(profiles) == 2
