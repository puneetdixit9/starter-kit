from flask import Response

from src.utils import log_user_access
from tests.unit_tests.base_unit_test import BaseUnitTest


class TestUnitUtils(BaseUnitTest):
    def test_log_user_access(self):
        with self.app.test_request_context("/test", method="GET"):
            response = Response("Hello, world!", status=200)
            logged_response = log_user_access(response)
            self.assertEqual(logged_response, response)
