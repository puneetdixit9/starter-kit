import pytest
from flask_jwt_extended import create_access_token
from pytest import raises

from main.custom_exceptions import RecordNotFoundError, UnauthorizedUserError
from main.modules.address.controller import AddressController
from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from tests.utils import get_address_data, get_updated_address_data

USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2


def get_user_and_headers(app, user_id: int = USER_ROLE_ID):
    with app.app_context():
        auth_user = AuthUser.query.filter_by(id=user_id).first()
        access_token = create_access_token(identity={"user_id": user_id})
        headers = {"Authorization": f"Bearer {access_token}"}
        return auth_user, headers


@pytest.fixture(scope="function")
def add_fixtures(load_data_from_file, load_data_to_model_using_controller_from_file):
    load_data_to_model_using_controller_from_file(
        AuthUserController.create_new_user, "unit_tests/fixtures/auth_users.json"
    )
    load_data_from_file(Address, "unit_tests/fixtures/addresses.json")


def test_delete_address(app, add_fixtures):
    with app.app_context():
        auth_user, _ = get_user_and_headers(app)
        response = AddressController.delete_address(1, auth_user)
        assert response == {"msg": "success"}


def test_create_new_address(app, add_fixtures):
    with app.app_context():
        address_data = get_address_data()
        address_id = AddressController.add_address(address_data)
        assert address_id == 3


def test_get_address(app, add_fixtures):
    with app.app_context():
        # get user with user role.
        auth_user, _ = get_user_and_headers(app)
        addresses = AddressController.get_addresses(auth_user)
        assert len(addresses) == 1

        # get user with admin role.
        auth_admin, _ = get_user_and_headers(app, ADMIN_ROLE_ID)
        addresses = AddressController.get_addresses(auth_admin)
        assert len(addresses) == 2

        with raises(RecordNotFoundError):
            # get address by invalid id
            AddressController.get_address_by_address_id(3, auth_user)

        with raises(UnauthorizedUserError):
            # get address by unauthorized user
            AddressController.get_address_by_address_id(2, auth_user)

        # get address by valid id
        address = AddressController.get_address_by_address_id(1, auth_user)
        assert address is not None
        assert address["type"] == "work"


def test_update_address(app, add_fixtures):
    with app.app_context():
        auth_user, _ = get_user_and_headers(app)
        updated_address = get_updated_address_data()

        address = AddressController.get_address_by_address_id(1, auth_user)
        # before updating the address
        assert address["type"] != updated_address["type"]

        response = AddressController.update_address(1, updated_address, auth_user)
        assert response == {"msg": "success"}

        address = AddressController.get_address_by_address_id(1, auth_user)
        # after updating
        assert address["type"] == updated_address["type"]
