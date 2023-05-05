import pytest

from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from tests.utils import (
    get_address_data,
    get_admin_role_login_credentials,
    get_user_role_login_credentials,
)


def get_headers(client, role: str = "user"):
    if role == "user":
        login_credentials = get_user_role_login_credentials()
    else:
        login_credentials = get_admin_role_login_credentials()
    response = client.post("/auth/login", json=login_credentials)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def add_fixtures(load_data_from_file, load_data_to_model_using_controller_from_file):
    load_data_to_model_using_controller_from_file(
        AuthUserController.create_new_user, "integration_tests/fixtures/auth_users.json"
    )
    load_data_from_file(Address, "integration_tests/fixtures/addresses.json")


def test_add_address(client, add_fixtures):
    headers = get_headers(client, "admin")
    response = client.post("/addresses", headers=headers, json=get_address_data())
    assert response.status_code == 201


def test_get_addresses(client, add_fixtures):
    headers = get_headers(client)
    response = client.get("/addresses", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_address_by_id(client, add_fixtures):
    headers = get_headers(client)
    response = client.get("/addresses/1", headers=headers)
    assert response.status_code == 200
    assert response.json["pin_code"] == 121106


def test_update_address(client, add_fixtures):
    headers = get_headers(client)

    response = client.get("/addresses/1", headers=headers)
    assert response.status_code == 200
    assert response.json["pin_code"] == 121106

    response = client.put("/addresses/1", headers=headers, json={"pin_code": 121107})
    assert response.status_code == 200

    response = client.get("/addresses/1", headers=headers)
    assert response.status_code == 200
    assert response.json["pin_code"] == 121107


def test_delete_address(client, add_fixtures):
    headers = get_headers(client)
    response = client.get("/addresses/1", headers=headers)
    assert response.status_code == 200

    response = client.delete("/addresses/1", headers=headers)
    assert response.status_code == 200

    response = client.get("/addresses/1", headers=headers)
    assert response.status_code == 404


def test_get_addresses_using_admin(client, add_fixtures):
    headers = get_headers(client, "admin")
    response = client.get("/addresses", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2


def test_unauthorized_user_error(client, add_fixtures):
    headers = get_headers(client, "admin")
    response = client.post("/addresses", headers=headers, json=get_address_data())
    assert response.status_code == 201

    headers = get_headers(client)
    response = client.get("/addresses/3", headers=headers)
    assert response.status_code == 401
