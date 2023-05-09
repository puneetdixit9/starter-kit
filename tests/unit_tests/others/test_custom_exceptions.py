from werkzeug.exceptions import HTTPException

from main.custom_exceptions.exception_handlers import (
    handle_exception,
    handle_record_not_found_error,
    handle_unauthorized_user_error,
    handle_validation_error,
)
from main.custom_exceptions.exceptions import (
    CustomValidationError,
    RecordNotFoundError,
    UnauthorizedUserError,
)


def test_handle_exception(app):
    with app.test_request_context():

        class TestException(HTTPException):
            pass

        response = handle_exception(TestException("test error"), app)
        assert response.status_code == 500


def test_handle_custom_exception_error(app):
    with app.test_request_context():
        response = handle_validation_error(CustomValidationError("test"))
        assert response.status_code == 400
        assert response.json["error"] == "test"


def test_handle_unauthorized_user_error(app):
    with app.test_request_context():
        response = handle_unauthorized_user_error(UnauthorizedUserError())
        assert response.status_code == 401
        assert response.json["error"] == "Unauthorized user"


def test_handle_record_not_found_error(app):
    with app.test_request_context():
        response = handle_record_not_found_error(RecordNotFoundError())
        assert response.status_code == 404
        assert response.json["error"] == "Record not found!!!"
