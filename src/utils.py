from flask import request
from marshmallow import ValidationError

import settings
from src.custom_exceptions import CustomValidationError
from src.logging_module.logger import get_logger

access_logger = get_logger("access", settings.INFO)


def update_class_object(obj, updated_dict):
    """
    This function is used to update any class object attributes with input key-value pair.
    :param obj:
    :param updated_dict:
    :return:
    """
    for k, v in updated_dict.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    return obj


def get_data_from_request_or_raise_validation_error(validator_schema, data) -> dict:
    """
    This function is used to get the and validate it according to its validator schema and
    return request data in dict form. Also, it is used to raise ValidationError (A Custom
    Exception) and return a complete error msg.
    :param validator_schema:
    :param data:
    :return:
    """
    try:
        validator = validator_schema()
        data = validator.load(data)
    except ValidationError as err:
        raise CustomValidationError(err)

    return data


def log_user_access(response):
    """
    This function is used by the flask app server to log each and every request in access_logger
    :param response:
    :return:
    """
    access_logger.info(
        f"User IP Address: {request.remote_addr} \n"
        f"Method: {request.method}\n"
        f"Path: {request.path}\n"
        f"Headers: {request.headers}"
        f"Request Payload: {request.get_data(as_text=True)}\n"
        f"Response data: {response.get_data(as_text=True)}\n"
        f"Status code: {response.status_code}"
    )
    return response
