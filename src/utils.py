from datetime import datetime

from flask import request
from marshmallow import ValidationError

import settings
from src.custom_exceptions import CustomValidationError
from src.logging_module.logger import get_logger

access_logger = get_logger("access", settings.INFO)


def update_class_object(obj, updated_dict):
    for k, v in updated_dict.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    if hasattr(obj, "updated_at"):
        setattr(obj, "updated_at", datetime.now())
    return obj


def get_data_from_request_or_raise_validation_error(validator_schema, data):
    try:
        validator = validator_schema()
        data = validator.load(data)
    except ValidationError as err:
        raise CustomValidationError(err)

    return data


def log_user_access(response):
    access_logger.info(
        f"User IP Address: {request.remote_addr} \n"
        f"Method: {request.method}\n"
        f"Status code: {response.status_code}\n"
        f"User Agent: {request.headers.get('User-Agent')}\n"
        f"Response data: {response.get_data(as_text=True)}"
    )

    return response
