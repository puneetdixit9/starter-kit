import operator
from datetime import datetime

from flask import request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields
from marshmallow.validate import Length
from sqlalchemy import between, or_

from main.custom_exceptions import CustomValidationError
from main.logging_module import INFO
from main.logging_module.logger import get_logger

access_logger = get_logger("access", INFO)


def validate_substr(v: str):
    """
    This function is used in schema validators to validate like field.
    :param v:
    :return:
    """
    if v.startswith("%") and v.endswith("%"):
        return True
    elif v.startswith("%"):
        return True
    elif v.endswith("%"):
        return True
    else:
        raise ValidationError("Like values must contain '%', e.g ['%example%', '%example', 'example%']")


def validate_not_dict_list_tuple(value: type):
    """
    This function is used in schema validators to validate the type of value.
    :param value:
    :return:
    """
    if isinstance(value, (dict, list, tuple)):
        raise ValidationError(f"Value {value} must not be a dict, list, or tuple")


def validate_int_float_date(value: int | float | str):
    """
    This function is used in schema validators to validate the type of value.
    :param value:
    :return:
    """
    if isinstance(value, str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            if not isinstance(value, (int, float)):
                raise ValidationError(f"Value {value} must be an int, float, or str('yyyy-mm-dd')")


class FiltersDataSchema(Schema):
    """
    Schema to validate filters data
    """

    eq = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    ne = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    lt = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    gt = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    lte = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    gte = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    between = fields.Dict(
        fields.String(),
        fields.List(fields.Field(validate=validate_int_float_date), validate=Length(equal=2)),
        required=False,
    )
    op_in = fields.Dict(
        fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False
    )
    nin = fields.Dict(fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False)
    null = fields.List(fields.String(), required=False)
    not_null = fields.List(fields.String(), required=False)
    op_or = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    substr = fields.Dict(fields.String(), fields.String(validate=validate_substr), required=False)


def get_data_from_request_or_raise_validation_error(validator_schema: type, data: dict) -> dict:
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


def add_filters_using_mapping(model: type, conditions: dict, filters: list, operator_key: str):
    """
    This function is used to update the filters using input and operators mapping.
    :param model: The SQLAlchemy model to add filters to.
    :param conditions:
    :param filters:
    :param operator_key:
    :return:
    """
    operator_mapping = {
        "eq": operator.eq,
        "ne": operator.ne,
        "lt": operator.lt,
        "lte": operator.le,
        "gt": operator.gt,
        "gte": operator.ge,
        # "contains": operator.contains,
        # "has_key": lambda x, y: y in x,
        # "any": any,
        # "has_all": lambda x, y: all(elem in x for elem in y),
    }

    logical_or_filters = []
    for column, value in conditions.items():
        if hasattr(model, column):
            if operator_key == "between":
                filters.append(between(getattr(model, column), value[0], value[1]))
            elif operator_key == "op_in":
                filters.append(getattr(model, column).in_(value))
            elif operator_key == "nin":
                filters.append(getattr(model, column).notin_(value))
            elif operator_key == "op_or":
                logical_or_filters.append(getattr(model, column) == value)
            elif operator_key == "substr":
                filters.append(getattr(model, column).like(value))
            else:
                filters.append(operator_mapping[operator_key](getattr(model, column), value))
    filters.append(or_(*logical_or_filters))


def add_filters_for_null_and_not_null(model: type, operator_key: str, conditions: dict, filters: list):
    """
    This function is used to add filters for null and not null values.
    :param model: The SQLAlchemy model to add filters to.
    :param operator_key:
    :param conditions:
    :param filters:
    :return:
    """
    for column in conditions:
        if hasattr(model, column):
            if operator_key == "null":
                filters.append(getattr(model, column) == None)  # noqa
            else:
                filters.append(getattr(model, column) != None)  # noqa


def get_query_including_filters(db: SQLAlchemy, model: type, filter_dict: dict):
    """
    This function is used to get the query with all filters
    :param db:
    :param model: The SQLAlchemy model to add filters to.
    :param filter_dict:
    :return:
    """
    try:
        validator = FiltersDataSchema()
        filter_dict = validator.load(filter_dict)
    except ValidationError as err:
        return err

    query = db.session.query(model)

    filters = []
    for operator_key, conditions in filter_dict.items():
        if operator_key == "null" or operator_key == "not_null":
            add_filters_for_null_and_not_null(model, operator_key, conditions, filters)
        else:
            add_filters_using_mapping(model, conditions, filters, operator_key)
    return query.filter(*filters)


# filters_dict = {
#     "eq": {
#         "type": "work",
#     },
#     "ne": {
#         "name": "Puneet"
#     },
#     "between": {
#         "age": [30, 50]
#     }
# }
#
# query = get_query_including_filters(db, Address, filters_dict)
