import pytest
from marshmallow import ValidationError
from pytest import raises

from main.custom_exceptions import CustomValidationError
from main.db import db
from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from main.utils import (
    FiltersDataSchema,
    access_logger,
    get_data_from_request_or_raise_validation_error,
    get_query_including_filters,
    log_user_access,
)


@pytest.fixture(scope="function")
def add_fixtures(load_data_from_file, load_data_to_model_using_controller_from_file):
    load_data_to_model_using_controller_from_file(
        AuthUserController.create_new_user, "unit_tests/fixtures/auth_users.json"
    )
    load_data_from_file(Address, "unit_tests/fixtures/addresses.json")


def test_get_generalize_query(app, add_fixtures):
    with app.app_context():
        # Invalid eq input.
        filters_dict = {"eq": {"id": {"invalid_key": "invalid value"}}}
        query = get_query_including_filters(db, Address, filters_dict)
        assert isinstance(query, ValidationError)

        # Invalid substr input.
        filters_dict = {"substr": {"type": "work"}}
        query = get_query_including_filters(db, Address, filters_dict)
        assert isinstance(query, ValidationError)

        filters_dict = {"lt": {"created_at": "20222-10-10", "id": []}}  # Invalid Date  # Invalid type
        query = get_query_including_filters(db, Address, filters_dict)
        assert isinstance(query, ValidationError)

        filters_dict = {
            "substr": {"type": "w%", "house_no_and_street": "%street%", "country": "%a"},
            "null": ["updated_at"],
            "not_null": ["id"],
            "op_in": {"id": [1, 2]},
            "nin": {"id": [4, 5]},
            "op_or": {
                "type": "work",
            },
            "gte": {"id": 1},
            "between": {"id": [0, 3]},
        }
        query = get_query_including_filters(db, Address, filters_dict)
        results = query.all()
        assert results is not None
        assert len(results) != 0


def test_get_data_from_request_or_raise_validation_error():
    with raises(CustomValidationError):
        request_data = {"lt": {"created_at": "20222-10-10", "id": []}}  # Invalid Date  # Invalid type
        get_data_from_request_or_raise_validation_error(FiltersDataSchema, request_data)

    request_data = {"lt": {"created_at": "2022-10-10", "id": 1}}
    data = get_data_from_request_or_raise_validation_error(FiltersDataSchema, request_data)
    assert data == request_data


def test_log_user_access(app, mocker):
    with app.test_request_context():
        mocker.patch.object(access_logger, "info")

        mock_request = mocker.Mock()
        mock_request.remote_addr = "127.0.0.1"
        mock_request.method = "GET"
        mock_request.path = "/test"
        mock_request.headers = {"Content-Type": "application/json"}
        mock_request.get_data.return_value = '{"key": "value"}'

        mock_response = mocker.Mock()
        mock_response.get_data.return_value = '{"result": "success"}'
        mock_response.status_code = 200

        result = log_user_access(mock_response)

        access_logger.info(
            "User IP Address: 127.0.0.1 \n"
            "Method: GET\n"
            "Path: /test\n"
            "Headers: {'Content-Type': 'application/json'}"
            "Request Payload: {'key': 'value'}\n"
            "Response data: {'result': 'success'}\n"
            "Status code: 200"
        )
        assert result == mock_response
