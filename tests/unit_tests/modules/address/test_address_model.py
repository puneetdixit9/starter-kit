import pytest
from flask_jwt_extended import create_access_token

from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from tests.utils import get_address_data

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


def test_get_all_address(app, add_fixtures):
    with app.app_context():
        addresses = Address.query.all()
        assert len(addresses) == 2


def test_add_address(app, add_fixtures):
    with app.app_context():
        address_data = get_address_data()
        address = Address.create(address_data)
        assert address.type == address_data["type"]
        addresses = Address.query.all()
        assert len(addresses) == 3
