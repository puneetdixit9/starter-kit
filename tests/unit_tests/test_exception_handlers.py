from unittest import TestCase

from flask import Flask
from werkzeug.exceptions import HTTPException

from src.custom_exceptions.exception_handlers import handle_exception


class TestExceptionHandler(TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_handle_exception(self):
        with self.app.test_request_context():

            class TestException(HTTPException):
                pass

            response = handle_exception(TestException("test error"), self.app)

            self.assertEqual(response.status_code, 500)
            self.assertIn("msg", response.json)
