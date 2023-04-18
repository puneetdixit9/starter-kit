from unittest.mock import patch

from flask_jwt_extended import verify_jwt_in_request

from src.database.models.auth import User
from src.managers.auth import AuthManager
from tests.unit_tests.base_unit_test import BaseUnitTest


class TestAuthManager(BaseUnitTest):
    def test_create_new_user(self):
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}

        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            user, error_data = AuthManager.create_new_user(user_data)

            saved_user = User.query.filter_by(email=user_data["email"]).first()
            self.assertIsNotNone(saved_user)

            self.assertEqual(saved_user.email, user_data["email"])
            self.assertEqual(saved_user.username, user_data["username"])
            self.assertEqual(saved_user.password, "test_hash_password")
            self.assertEqual(saved_user.role, user_data["role"])

            self.assertEqual(user, saved_user)
            self.assertEqual(error_data, {})

    def test_get_token(self):
        user, headers = self.get_user_and_headers()

        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            invalid_login_data = {
                "username": "invalidtestuser",
                "password": "testpassword",
            }
            response_data, error_msg = AuthManager.get_token(invalid_login_data)
            self.assertEqual(response_data, {})
            self.assertEqual(error_msg, "user not found with invalidtestuser")

            with patch("src.managers.auth.check_password_hash") as mock_check_password_hash:
                mock_check_password_hash.side_effect = [True, False]
                login_data = {
                    "username": "testuser",
                    "password": "testpassword",
                }
                response_data, error_msg = AuthManager.get_token(login_data)
                self.assertIn("access_token", response_data)
                self.assertIn("refresh_token", response_data)

                login_data["password"] = "wrong_password"
                response_data, error_msg = AuthManager.get_token(login_data)
                self.assertEqual(response_data, {})
                self.assertEqual(error_msg, "wrong password")

    def test_get_current_user(self):
        user, headers = self.get_user_and_headers()
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            current_user = AuthManager.get_current_user()
            self.assertEqual(current_user, user)

    def test_get_current_user_profile(self):
        user, headers = self.get_user_and_headers()

        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            expected_profile = user.as_dict()
            current_user_profile = AuthManager.get_current_user_profile()
            self.assertEqual(current_user_profile, expected_profile)

    def test_update_user_profile(self):
        user, headers = self.get_user_and_headers()

        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            updated_user_data = {
                "first_name": "updated_test@example.com",
                "last_name": "updated_testuser",
            }
            AuthManager.update_user_profile(updated_user_data)

            updated_user = User.query.filter_by(id=user.id).first()
            self.assertEqual(updated_user.first_name, updated_user_data["first_name"])
            self.assertEqual(updated_user.last_name, updated_user_data["last_name"])

    def test_update_user_password(self):
        user, headers = self.get_user_and_headers()
        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            with self.app.test_request_context(headers=headers):
                verify_jwt_in_request()
                update_data = {"old_password": "testpassword", "new_password": "newpassword"}
                with patch("src.managers.auth.check_password_hash") as mock_check_password_hash:
                    mock_check_password_hash.side_effect = [True, False]
                    mock_generate_password_hash.return_value = "test_updated_hash_password"
                    response_data, error_msg = AuthManager.update_user_password(update_data)
                    updated_user = User.query.filter_by(id=user.id).first()
                    self.assertEqual(updated_user.password, "test_updated_hash_password")
                    self.assertEqual(response_data, {"status": "success"})
                    self.assertEqual(error_msg, "")

    def test_change_password_old_and_new_both_same(self):
        user, headers = self.get_user_and_headers()
        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            with self.app.test_request_context(headers=headers):
                verify_jwt_in_request()
                update_data = {"old_password": "testpassword", "new_password": "testpassword"}
                with patch("src.managers.auth.check_password_hash") as mock_check_password_hash:
                    mock_check_password_hash.side_effect = [True, True]
                    mock_generate_password_hash.return_value = "test_hash_password"
                    response_data, error_msg = AuthManager.update_user_password(update_data)
                    self.assertEqual(response_data, {})
                    self.assertEqual(error_msg, "new password can not same as old password")

    def test_change_password_with_invalid_old_password(self):
        user, headers = self.get_user_and_headers()
        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            with self.app.test_request_context(headers=headers):
                verify_jwt_in_request()
                update_data = {"old_password": "invalidpassword", "new_password": "testpassword"}
                with patch("src.managers.auth.check_password_hash") as mock_check_password_hash:
                    mock_check_password_hash.return_value = False
                    mock_generate_password_hash.return_value = "test_hash_password"
                    response_data, error_msg = AuthManager.update_user_password(update_data)
                    self.assertEqual(response_data, {})
                    self.assertEqual(error_msg, "Old password is invalid")
