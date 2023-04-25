from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf

from main.utils import (
    validate_int_float_date,
    validate_like,
    validate_not_dict_list_tuple,
)


class AddAddressSchema(Schema):
    """
    Schema to add address to the database.
    """

    type = fields.String(validate=OneOf(["home", "work", "other"]), required=True)
    house_no_and_street = fields.String(required=True)
    landmark = fields.String(required=False)
    country = fields.String(required=True)

    pin_code = fields.Integer(required=True)


class UpdateAddressSchema(Schema):
    """
    Schema to update the address.
    """

    type = fields.String(validate=OneOf(["home", "work", "other"]), required=False)
    house_no_and_street = fields.String(required=False)
    landmark = fields.String(required=False)
    country = fields.String(required=False)
    pin_code = fields.Integer(required=False)


class FiltersDataSchema(Schema):
    """
    Schema to validate filters data
    """

    equal = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    not_equal = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    less_than = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    greater_than = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    less_than_or_equal = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    greater_than_or_equal = fields.Dict(fields.String(), fields.Field(validate=validate_int_float_date), required=False)
    between = fields.Dict(
        fields.String(),
        fields.List(fields.Field(validate=validate_int_float_date), validate=Length(equal=2)),
        required=False,
    )
    in_list = fields.Dict(
        fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False
    )
    not_in_list = fields.Dict(
        fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False
    )
    is_null = fields.List(fields.String(), required=False)
    is_not_null = fields.List(fields.String(), required=False)
    logical_or = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    like = fields.Dict(fields.String(), fields.String(validate=validate_like), required=False)
