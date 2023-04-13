import unittest

from marshmallow import ValidationError

from src.schema_validators.auth import LogInSchema


class TestLogInSchema(unittest.TestCase):
    def test_required_password_field(self):
        schema = LogInSchema()
        with self.assertRaises(ValidationError) as context:
            schema.load({"username": "testuser", "email": "test@test.com"})
        self.assertTrue("Missing data for required field." in str(context.exception))

    def test_at_least_one_param_required(self):
        schema = LogInSchema()
        with self.assertRaises(ValidationError) as context:
            schema.load({"password": "testpassword"})
        self.assertTrue("At least one param is required from ['email', 'username']" in str(context.exception))

    def test_valid_data(self):
        schema = LogInSchema()
        data = schema.load({"username": "testuser", "password": "testpassword"})
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["password"], "testpassword")

    def test_invalid_email(self):
        schema = LogInSchema()
        with self.assertRaises(ValidationError) as context:
            schema.load({"email": "invalid_email", "password": "testpassword"})
        self.assertTrue("Not a valid email address." in str(context.exception))
