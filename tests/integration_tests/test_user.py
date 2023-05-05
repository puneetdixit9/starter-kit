import pytest

from main.modules.auth.controller import AuthUserController
from tests.utils import (
    get_admin_role_login_credentials,
    get_update_profile_data,
    get_user_role_login_credentials,
)


def get_headers(client, role: str = AuthUserController.ROLES.USER.value):
    if role == AuthUserController.ROLES.USER.value:
        login_credentials = get_user_role_login_credentials()
    else:
        login_credentials = get_admin_role_login_credentials()
    response = client.post("/auth/login", json=login_credentials)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def add_fixtures(load_data_to_model_using_controller_from_file):
    load_data_to_model_using_controller_from_file(
        AuthUserController.create_new_user, "integration_tests/fixtures/auth_users.json"
    )


def test_get_user_profile(client, add_fixtures):
    headers = get_headers(client)
    response = client.get("/users/profile", headers=headers)
    assert response.status_code == 200


def test_update_user_profile(client, add_fixtures):
    headers = get_headers(client)
    response = client.put("/users/profile", headers=headers, json=get_update_profile_data())
    assert response.status_code == 200


def test_get_all_users_profiles(client, add_fixtures):
    headers = get_headers(client, role=AuthUserController.ROLES.ADMIN.value)
    response = client.get("/users/profiles", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_users_profile_by_id(client, add_fixtures):
    headers = get_headers(client, role=AuthUserController.ROLES.ADMIN.value)
    response = client.get("/users/profiles/1", headers=headers)
    assert response.status_code == 200

    response = client.get("/users/profiles/2", headers=headers)
    assert response.status_code == 200


def test_update_users_profile_by_id(client, add_fixtures):
    headers = get_headers(client, role=AuthUserController.ROLES.ADMIN.value)
    response = client.put("/users/profiles/1", headers=headers, json=get_update_profile_data())
    assert response.status_code == 200

    response = client.put("/users/profiles/2", headers=headers, json=get_update_profile_data())
    assert response.status_code == 200
