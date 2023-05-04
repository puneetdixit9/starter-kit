import pytest

from main.modules.auth.model import AuthUser
from tests.utils import get_user_role_login_credentials, get_user_role_signup_data


class TestAuthView:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file):
        load_data_from_file(AuthUser, "integration_tests/fixtures/auth_users.json")

    def test_signup_success(self, client):
        signup_data = get_user_role_signup_data()
        response = client.post("/auth/signup", json=signup_data)
        assert response.status_code == 201

    def test_signup_failure_minimum_password_length(self, client):
        signup_data = get_user_role_signup_data()
        signup_data["password"] = "123"
        response = client.post("/auth/signup", json=signup_data)
        assert response.status_code == 400
        assert response.json["error"] == "{'password': ['Shorter than minimum length 8.']}"

    def test_signup_user_already_exists(self, client):
        signup_data = get_user_role_signup_data()
        response = client.post("auth/signup", json=signup_data)
        assert response.status_code == 409
        assert response.json["error"] == "user already exists with provided username"

    def test_login_success(self, client):
        login_data = get_user_role_login_credentials()
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200

    def test_login_failure_with_wrong_email(self, client):
        login_data = get_user_role_login_credentials()
        login_data["email"] = "wrongemail@gmail.com"
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 403
        assert response.json["error"] == "user not found with wrongemail@gmail.com"
