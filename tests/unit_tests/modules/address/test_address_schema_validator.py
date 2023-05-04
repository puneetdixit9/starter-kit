import pytest
from marshmallow import ValidationError

from main.modules.address.schema_validator import AddAddressSchema, UpdateAddressSchema


class TestAddressSchemaValidators:
    def test_add_address_schema(self):
        schema = AddAddressSchema()

        # Test valid input data
        valid_data = {
            "type": "home",
            "house_no_and_street": "123 Test Street",
            "landmark": "Near Test Park",
            "country": "Test Country",
            "pin_code": 123456,
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "type": "invalid_type",  # Invalid type value
            "house_no_and_street": "123 Test Street",
            "landmark": "Near Test Park",
            "country": "Test Country",
            "pin_code": 123456,
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)

    def test_update_address_schema(self):
        schema = UpdateAddressSchema()

        # Test valid input data
        valid_data = {
            "type": "home",
            "house_no_and_street": "123 Test Street",
            "landmark": "Near Test Park",
            "country": "Test Country",
            "pin_code": 123456,
        }
        result = schema.load(valid_data)
        assert result == valid_data

        # Test invalid input data
        invalid_data = {
            "type": "invalid_type",  # Invalid type value
            "house_no_and_street": "123 Test Street",
            "landmark": "Near Test Park",
            "country": "Test Country",
            "pin_code": 123456,
        }
        with pytest.raises(ValidationError):
            schema.load(invalid_data)
