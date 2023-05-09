from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from tests.utils import get_update_password_data


def get_user_and_headers(app):
    with app.app_context():
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        user, error_data = AuthUserController.create_new_user(user_data)
        access_token = create_access_token(identity={"user_id": user.id})
        headers = {"Authorization": f"Bearer {access_token}"}
        return user, headers


def test_create_new_user(app, mocker):
    with app.app_context():
        user_data = {"email": "test1@example.com", "username": "test1", "password": "testpassword", "role": "user"}

        # Replace generate_password_hash with a mock
        mock_generate_password_hash = mocker.patch("main.modules.auth.controller.generate_password_hash")
        mock_generate_password_hash.return_value = "test_hash_password"

        # Call create_new_user and check the result
        user, error = AuthUserController.create_new_user(user_data)
        saved_user = AuthUser.query.filter_by(email=user_data["email"]).first()
        assert saved_user is not None
        assert saved_user.email == user_data["email"]
        assert saved_user.username == user_data["username"]
        assert saved_user.password == "test_hash_password"
        assert saved_user.role == user_data["role"]
        assert user is saved_user
        assert error == {}

        user, error = AuthUserController.create_new_user(user_data)
        assert user is None
        assert error == {"error": "user already exists with provided username"}


def test_get_current_user(app):
    user, headers = get_user_and_headers(app)
    with app.test_request_context(headers=headers):
        verify_jwt_in_request()
        current_user = AuthUserController.get_current_auth_user()
        assert current_user.serialize() == user.serialize()


def test_update_user_password(app, mocker):
    user, headers = get_user_and_headers(app)
    with app.test_request_context(headers=headers):
        verify_jwt_in_request()
        mock_generate_password_hash = mocker.patch("main.modules.auth.controller.check_password_hash")
        mock_generate_password_hash.side_effect = [True, False]

        update_password_data = get_update_password_data()
        response, error = AuthUserController.update_user_password(update_password_data)
        assert response == {"status": "success"}
        assert error == ""

        mock_generate_password_hash.side_effect = [True, True]
        update_password_data = get_update_password_data()
        response, error = AuthUserController.update_user_password(update_password_data)
        assert response == {}
        assert error == "new password can not same as old password"

        mock_generate_password_hash.side_effect = [False, True]
        update_password_data = get_update_password_data()
        response, error = AuthUserController.update_user_password(update_password_data)
        assert response == {}
        assert error == "Old password is invalid"


def test_get_token(app):
    get_user_and_headers(app)  # to create a user
    with app.test_request_context():
        login_data = {"username": "testuser", "password": "testpassword"}
        token, error = AuthUserController.get_token(login_data)
        assert error == ""
        assert isinstance(token, dict)
        assert "access_token" in token
        assert "refresh_token" in token

        login_data = {"username": "invalid_username", "password": "testpassword"}
        token, error = AuthUserController.get_token(login_data)
        assert error == "user not found with invalid_username"

        login_data = {"username": "testuser", "password": "wrong_password"}
        token, error = AuthUserController.get_token(login_data)
        assert error == "wrong password"


def test_get_access_token_from_refresh_token(app):
    _, headers = get_user_and_headers(app)
    with app.test_request_context(headers=headers):
        verify_jwt_in_request()
        response = AuthUserController.refresh_access_token()
        assert isinstance(response, dict)
        assert "access_token" in response


def test_logout(app):
    _, headers = get_user_and_headers(app)
    with app.test_request_context(headers=headers):
        verify_jwt_in_request()
        response = AuthUserController.logout()
        assert isinstance(response, dict)
        assert response["msg"] == "Access token successfully revoked"
