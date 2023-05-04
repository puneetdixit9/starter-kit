import pytest
from marshmallow import ValidationError

from main.modules.auth.schema_validator import LogInSchema, SignUpSchema, UpdatePassword


class TestAuthSchemaValidators:
    def test_sign_up_schema(self):
        schema = SignUpSchema()

        # Test valid input data
        valid_data = {
            "first_name": "test",
            "last_name": "test",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "password": "password",
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "role": "invalid_role",  # Invalid role value
            "password": "password",
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)

    def test_log_in_schema(self):
        schema = LogInSchema()

        # Test valid input data with email
        valid_data = {
            "email": "test@example.com",
            "password": "password",
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test valid input data with username
        valid_data = {
            "username": "testuser",
            "password": "password",
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "password": "password",
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)

    def test_update_password_schema(self):
        schema = UpdatePassword()

        # Test valid input data
        valid_data = {
            "old_password": "old_password",
            "new_password": "new_password",
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "new_password": "new_password",
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)

        invalid_data = {
            "old_password": "old_password",
            "new_password": "short",
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)
