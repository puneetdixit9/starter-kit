import pytest

from main.modules.auth.controller import AuthUserController
from tests.utils import (
    get_update_password_data,
    get_user_role_login_credentials,
    get_user_role_signup_data,
)


def get_headers(client, with_refresh_token=False):
    login_credentials = get_user_role_login_credentials()
    response = client.post("/auth/login", json=login_credentials)
    assert response.status_code == 200
    if with_refresh_token:
        return {"Authorization": f"Bearer {response.json['refresh_token']}"}
    return {"Authorization": f"Bearer {response.json['access_token']}"}


@pytest.fixture(scope="function")
def add_fixtures(load_data_to_model_using_controller_from_file):
    load_data_to_model_using_controller_from_file(
        AuthUserController.create_new_user, "integration_tests/fixtures/auth_users.json"
    )


def test_login_success(client, add_fixtures):
    login_data = get_user_role_login_credentials()
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200


def test_login_failure(client, add_fixtures):
    login_data = get_user_role_login_credentials()
    login_data["password"] = "wrong_password"
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 403

    del login_data["email"]
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 400


def test_update_password(client, add_fixtures):
    headers = get_headers(client)
    response = client.put("/auth/change_password", headers=headers, json=get_update_password_data())
    assert response.status_code == 200


def test_failure_update_password(client, add_fixtures):
    headers = get_headers(client)

    updated_password_data = get_update_password_data()
    updated_password_data["new_password"] = updated_password_data["old_password"]
    response = client.put("/auth/change_password", headers=headers, json=updated_password_data)
    assert response.status_code == 401

    updated_password_data["old_password"] = "wrong_old_password"
    response = client.put("/auth/change_password", headers=headers, json=updated_password_data)
    assert response.status_code == 401


def test_signup_success(client, add_fixtures):
    signup_data = get_user_role_signup_data()
    response = client.post("/auth/signup", json=signup_data)
    assert response.status_code == 201


def test_signup_failure_minimum_password_length(client, add_fixtures):
    signup_data = get_user_role_signup_data()
    signup_data["password"] = "123"
    response = client.post("/auth/signup", json=signup_data)
    assert response.status_code == 400
    assert response.json["error"] == "{'password': ['Shorter than minimum length 8.']}"


def test_signup_user_already_exists(client, add_fixtures):
    signup_data = get_user_role_signup_data()
    response = client.post("auth/signup", json=signup_data)
    assert response.status_code == 201

    response = client.post("auth/signup", json=signup_data)  # again trying to signup with same data
    assert response.status_code == 409
    assert response.json["error"] == "user already exists with provided username"


def test_login_failure_with_wrong_email(client, add_fixtures):
    login_data = get_user_role_login_credentials()
    login_data["email"] = "wrongemail@gmail.com"
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 403
    assert response.json["error"] == "user not found with wrongemail@gmail.com"


def test_get_access_token_using_refresh_token(client, add_fixtures):
    headers = get_headers(client, with_refresh_token=True)
    response = client.get("/auth/refresh", headers=headers)
    assert response.status_code == 200


def test_logout(client, add_fixtures):
    headers = get_headers(client, with_refresh_token=True)
    response = client.delete("/auth/logout", headers=headers)
    assert response.status_code == 200
