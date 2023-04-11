from flask import jsonify, request


def handle_exception(e, app):
    request_data = {
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'payload': request.get_data().decode('utf-8')
    }
    app.logger.exception(f"Request data: {request_data}, error:  {e}")
    response = jsonify({"message": "Internal Server Error."})
    response.status_code = 500
    return response


def handle_validation_error(error):
    response = jsonify({
        'error': str(error),
    })
    response.status_code = error.status_code
    return response
