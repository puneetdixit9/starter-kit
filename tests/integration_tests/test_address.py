import pytest

from main.modules.address.model import Address
from tests.utils import (
    get_address_data,
    get_user_role_login_credentials,
    get_user_role_signup_data,
)


def get_headers(client):
    response = client.post("/auth/login", json=get_user_role_login_credentials())
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json['access_token']}", "Content-Type": "application/json"}


class TestAuthView:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file, client):
        client.post("/auth/signup", json=get_user_role_signup_data())
        load_data_from_file(Address, "integration_tests/fixtures/addresses.json")

    def test_get_addresses(self, client):
        headers = get_headers(client)
        response = client.get("/addresses", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_add_address(self, client):
        headers = get_headers(client)
        response = client.post("/addresses", headers=headers, json=get_address_data())
        assert response.status_code == 201
