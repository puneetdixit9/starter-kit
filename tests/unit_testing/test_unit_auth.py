from unittest.mock import patch

from flask_jwt_extended import create_access_token, verify_jwt_in_request

from src.database.models.auth import User
from src.managers.auth import AuthManager
from tests.unit_testing.base_unit_test import BaseUnitTest


class TestAuthManager(BaseUnitTest):
    def test_create_new_user(self):
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}

        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            user, error_data = AuthManager.create_new_user(user_data)

            # assert that the user is saved in the database
            saved_user = User.query.filter_by(email=user_data["email"]).first()
            self.assertIsNotNone(saved_user)

            # assert that the saved user data is correct
            self.assertEqual(saved_user.email, user_data["email"])
            self.assertEqual(saved_user.username, user_data["username"])
            self.assertEqual(saved_user.password, "test_hash_password")
            self.assertEqual(saved_user.role, user_data["role"])

            # assert that the returned user and error data is correct
            self.assertEqual(user, saved_user)
            self.assertEqual(error_data, {})

    def test_get_current_user(self):
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        user, error_data = AuthManager.create_new_user(user_data)
        access_token = create_access_token(identity={"user_id": user.id})
        headers = {"Authorization": f"Bearer {access_token}"}
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            current_user = AuthManager.get_current_user()
            self.assertEqual(current_user, user)

    def test_get_current_user_profile(self):
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        user, error_data = AuthManager.create_new_user(user_data)
        access_token = create_access_token(identity={"user_id": user.id})
        headers = {"Authorization": f"Bearer {access_token}"}

        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            expected_profile = user.as_dict()
            current_user_profile = AuthManager.get_current_user_profile()
            self.assertEqual(current_user_profile, expected_profile)

    def test_update_user_profile(self):
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        user, error_data = AuthManager.create_new_user(user_data)
        access_token = create_access_token(identity={"user_id": user.id})
        headers = {"Authorization": f"Bearer {access_token}"}

        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            # update user profile
            updated_user_data = {
                "first_name": "updated_test@example.com",
                "last_name": "updated_testuser",
            }
            AuthManager.update_user_profile(updated_user_data)

            # assert that the user data has been updated in the database
            updated_user = User.query.filter_by(id=user.id).first()
            self.assertEqual(updated_user.first_name, updated_user_data["first_name"])
            self.assertEqual(updated_user.last_name, updated_user_data["last_name"])
