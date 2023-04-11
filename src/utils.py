from datetime import datetime
from marshmallow import ValidationError
from src.custom_exceptions import CustomValidationError


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
