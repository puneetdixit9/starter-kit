import pytest

from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from tests.utils import get_address_data, get_user_role_signup_data

TEST_USER_ID = 1


class TestAddressModel:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file, app):
        with app.app_context():
            user, _ = AuthUserController.create_new_user(get_user_role_signup_data())
        load_data_from_file(Address, "unit_tests/fixtures/addresses.json")

    def test_get_all_address(self, app):
        with app.app_context():
            addresses = Address.query.all()
            assert len(addresses) == 2

    def test_add_address(self, app):
        with app.app_context():
            address_data = get_address_data()
            address = Address.create(address_data)
            assert address.type == address_data["type"]
            addresses = Address.query.all()
            assert len(addresses) == 3
