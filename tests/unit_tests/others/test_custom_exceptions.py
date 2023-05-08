from werkzeug.exceptions import HTTPException

from main.custom_exceptions.exception_handlers import handle_exception


def test_handle_exception(app):
    with app.test_request_context():

        class TestException(HTTPException):
            pass

        response = handle_exception(TestException("test error"), app)
        assert response.status_code == 500
