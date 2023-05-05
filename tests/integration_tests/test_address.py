import pytest

from main.modules.address.model import Address
from tests.utils import (
    get_address_data,
    get_admin_role_login_credentials,
    get_admin_role_signup_data,
    get_user_role_login_credentials,
    get_user_role_signup_data,
)


def get_headers(client, role: str = "user"):
    if role == "user":
        login_credentials = get_user_role_login_credentials()
    else:
        login_credentials = get_admin_role_login_credentials()
    response = client.post("/auth/login", json=login_credentials)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}", "Content-Type": "application/json"}


class TestAuthView:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file, client):
        client.post("/auth/signup", json=get_user_role_signup_data())
        client.post("/auth/signup", json=get_admin_role_signup_data())
        load_data_from_file(Address, "integration_tests/fixtures/addresses.json")

    def test_add_address(self, client, nested_transaction):
        headers = get_headers(client, "admin")
        response = client.post("/addresses", headers=headers, json=get_address_data())
        assert response.status_code == 201

    def test_get_addresses(self, client, nested_transaction):
        headers = get_headers(client)
        response = client.get("/addresses", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_get_address_by_id(self, client, nested_transaction):
        headers = get_headers(client)
        response = client.get("/addresses/1", headers=headers)
        assert response.status_code == 200
        assert response.json["pin_code"] == 121106

    def test_update_address(self, client, nested_transaction):
        headers = get_headers(client)

        response = client.get("/addresses/1", headers=headers)
        assert response.status_code == 200
        assert response.json["pin_code"] == 121106

        response = client.put("/addresses/1", headers=headers, json={"pin_code": 121107})
        assert response.status_code == 200

        response = client.get("/addresses/1", headers=headers)
        assert response.status_code == 200
        assert response.json["pin_code"] == 121107

    # def test_delete_address(self, client):
    #     headers = get_headers(client)
    #     response = client.get("/addresses/1", headers=headers)
    #     assert response.status_code == 200
    #
    #     response = client.delete("/addresses/1", headers=headers)
    #     assert response.status_code == 200
    #
    #     response = client.get("/addresses/1", headers=headers)
    #     assert response.status_code == 404

    def test_get_addresses_using_admin(self, client, nested_transaction):
        headers = get_headers(client, "admin")
        response = client.get("/addresses", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_unauthorized_user_error(self, client, nested_transaction):
        headers = get_headers(client, "admin")
        response = client.post("/addresses", headers=headers, json=get_address_data())
        assert response.status_code == 201

        headers = get_headers(client)
        response = client.get("/addresses/3", headers=headers)
        assert response.status_code == 401
