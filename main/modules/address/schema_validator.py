from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf

from main.utils import (
    validate_int_float_date,
    validate_not_dict_list_tuple,
    validate_substr,
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
    in_ = fields.Dict(fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False)
    nin = fields.Dict(fields.String(), fields.List(fields.Field(validate=validate_not_dict_list_tuple)), required=False)
    null = fields.List(fields.String(), required=False)
    not_null = fields.List(fields.String(), required=False)
    or_ = fields.Dict(fields.String(), fields.Field(validate=validate_not_dict_list_tuple), required=False)
    substr = fields.Dict(fields.String(), fields.String(validate=validate_substr), required=False)
