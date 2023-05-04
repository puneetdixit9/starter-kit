import pytest
from flask_jwt_extended import create_access_token

from main.modules.address.controller import AddressController
from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from tests.utils import get_address_data, get_user_role_signup_data

USER_ROLE_ID = None
ADMIN_ROLE_ID = None


def get_user_and_headers(app):
    with app.app_context():
        auth_user = AuthUser.query.filter_by(id=USER_ROLE_ID).first()
        access_token = create_access_token(identity={"user_id": USER_ROLE_ID})
        headers = {"Authorization": f"Bearer {access_token}"}
        return auth_user, headers


class TestAddressController:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file, app):
        global USER_ROLE_ID
        with app.app_context():
            user, _ = AuthUserController.create_new_user(get_user_role_signup_data())
            USER_ROLE_ID = user.id
        load_data_from_file(Address, "unit_tests/fixtures/addresses.json")

    def test_create_new_address(self, app):
        with app.app_context():
            _, headers = get_user_and_headers(app)
            with app.test_request_context(headers=headers):
                address_data = get_address_data()
                address_id = AddressController.add_address(address_data)
                assert address_id == 3

    def test_get_address(self, app):
        with app.app_context():
            auth_user, headers = get_user_and_headers(app)
            with app.test_request_context(headers=headers):
                addresses = AddressController.get_addresses(auth_user)
                assert len(addresses) == 2
