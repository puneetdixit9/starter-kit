import pytest
from marshmallow import ValidationError

from main.modules.user.schema_validator import UpdateProfile


class TestUpdateProfileSchemaValidators:
    def test_update_profile_schema(self):
        schema = UpdateProfile()

        # Test valid input data
        valid_data = {
            "first_name": "test",
            "last_name": "test",
            "department": "test",
            "function": "test",
            "role": "user",
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "role": "invalid_role",
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)
