from unittest.mock import MagicMock

from flask import Response
from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.modules.address.controller import AddressController
from main.modules.address.view import AddressApi, AddressApi2
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


class TestAddressApi:
    def setup_method(self):
        self.api = AddressApi()

    def test_get(self, app):
        _, headers = get_user_and_headers(app)

        # Mock the get_addresses method of the AddressController class
        AddressController.get_addresses = MagicMock(return_value=[])

        # Make a GET request to the endpoint
        with app.test_request_context("/addresses", headers=headers):
            verify_jwt_in_request()
            response = self.api.get()

        # Check that the response is a JSON object
        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.json == []

    def test_post(self, app, mocker):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.id = 123

        # Mock the get_current_auth_user method to return the mock user object
        mocker.patch.object(AuthUserController, "get_current_auth_user", return_value=mock_user)

        # Mock the add_address method of the AddressController class
        mocker.patch.object(AddressController, "add_address", return_value=1)

        # Make a POST request to the endpoint
        address_data = get_address_data()

        _, headers = get_user_and_headers(app)
        with app.test_request_context("/addresses", json=address_data, headers=headers):
            verify_jwt_in_request()
            response = self.api.post()

        # Check that the response is a JSON object and contains the expected data
        assert isinstance(response, Response)
        assert response.status_code == 201
        assert response.json == {"message": "Address added", "location": "/addresses/1", "id": 1}


class TestAddressApi2:
    def setup_method(self):
        self.api = AddressApi2()

    def test_get(self, app, mocker):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.id = 123

        # Mock the get_current_auth_user method to return the mock user object
        mocker.patch.object(AuthUserController, "get_current_auth_user", return_value=mock_user)

        # Mock the get_address_by_address_id method of the AddressController class
        mocker.patch.object(
            AddressController, "get_address_by_address_id", return_value={"id": 1, "street": "123 Main St"}
        )

        # Make a GET request to the endpoint
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/addresses/1", headers=headers):
            verify_jwt_in_request()
            response = self.api.get(1)

        # Check that the response is a JSON object and contains the expected data
        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.json == {"id": 1, "street": "123 Main St"}

    def test_put(self, app, mocker):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.id = 123

        # Mock the get_current_auth_user method to return the mock user object
        mocker.patch.object(AuthUserController, "get_current_auth_user", return_value=mock_user)

        # Mock the update_address method of the AddressController class
        mocker.patch.object(AddressController, "update_address", return_value={"msg": "success"})

        # Make a PUT request to the endpoint
        _, headers = get_user_and_headers(app)
        address_data = {
            "type": "work",
            "house_no_and_street": "75, street 4",
            "country": "India",
            "pin_code": 121106,
        }
        with app.test_request_context("/addresses/1", method="PUT", headers=headers, json=address_data):
            verify_jwt_in_request()
            response = self.api.put(1)

        # Check that the response is a JSON object and contains the expected data
        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.json == {"msg": "success"}

    def test_delete(self, app, mocker):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.id = 123

        # Mock the get_current_auth_user method to return the mock user object
        mocker.patch.object(AuthUserController, "get_current_auth_user", return_value=mock_user)

        # Mock the create_address method of the AddressController class
        mocker.patch.object(AddressController, "delete_address", return_value={"msg": "success"})

        # Make a POST request to the endpoint
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/addresses", headers=headers):
            verify_jwt_in_request()
            response = self.api.delete(1)

        # Check that the response is a JSON object and contains the expected data
        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.json == {"msg": "success"}
