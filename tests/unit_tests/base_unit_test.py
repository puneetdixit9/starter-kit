import os
import unittest
from unittest.mock import patch

from flask_jwt_extended import create_access_token

import settings
from server import get_app
from src.database import db as _db
from src.managers.auth import AuthManager
from tests.integration_tests.test_utils import get_login_data, get_signup_data


class BaseUnitTest(unittest.TestCase):
    app = get_app(settings.TEST_CONFIG)

    def add_fixtures(self):
        pass

    def setUp(self):
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        _db.create_all()
        self.add_fixtures()

    def tearDown(self):
        self.app_context.pop()
        with self.app.app_context():
            _db.engine.dispose()
        path = os.getcwd().replace("\\tests\\unit_tests", "")
        os.remove(path + "\\instance\\test_db.sqlite")

    def signup(self):
        signup_data = get_signup_data()
        response = self.client.post("/signup", json=signup_data)
        self.assertEqual(response.status_code, 201)

    def login(self):
        self.signup()
        login_data = get_login_data()
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 200)
        return response.json

    @staticmethod
    def get_user_and_headers():
        user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword", "role": "user"}
        with patch("src.managers.auth.generate_password_hash") as mock_generate_password_hash:
            mock_generate_password_hash.return_value = "test_hash_password"
            user, error_data = AuthManager.create_new_user(user_data)
            access_token = create_access_token(identity={"user_id": user.id})
            headers = {"Authorization": f"Bearer {access_token}"}
            return user, headers
