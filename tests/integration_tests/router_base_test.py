import os
import unittest

import settings
from server import get_app
from src.database import db as _db
from tests.integration_tests.test_utils import get_login_data, get_signup_data


class BaseRouterTest(unittest.TestCase):
    app = get_app(settings.TEST_CONFIG)

    def setUp(self):
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            _db.create_all()

    def tearDown(self):
        with self.app.app_context():
            _db.engine.dispose()
        path = os.getcwd().replace("\\tests\\integration_tests", "")
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
