from flask import jsonify, request
from werkzeug.exceptions import NotFound


def create_error_response(error):
    response = jsonify(
        {
            "error": str(error),
        }
    )
    response.status_code = error.status_code
    return response


#  below are the handlers for custom exception classes.


def handle_exception(e, app):
    if isinstance(e, NotFound):
        return jsonify(error=e.description), e.code
    request_data = {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "payload": request.get_data().decode("utf-8"),
    }
    app.logger.exception(f"Request data: {request_data}, error:  {e}")
    response = jsonify({"msg": "Internal Server Error."})
    response.status_code = 500
    return response


def handle_validation_error(error):
    return create_error_response(error)


def handle_unauthorized_user_error(error):
    return create_error_response(error)


def handle_record_not_found_error(error):
    return create_error_response(error)
