from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser


def get_user_and_headers(app):
    with app.app_context():
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        user, error_data = AuthUserController.create_new_user(user_data)
        access_token = create_access_token(identity={"user_id": user.id})
        headers = {"Authorization": f"Bearer {access_token}"}
        return user, headers


class TestAuthController:
    def test_create_new_user(self, app, mocker):
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

    def test_get_current_user(self, app):
        user, headers = get_user_and_headers(app)
        with app.test_request_context(headers=headers):
            verify_jwt_in_request()
            current_user = AuthUserController.get_current_auth_user()
            assert current_user.serialize() == user.serialize()
