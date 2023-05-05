from marshmallow import Schema, fields
from marshmallow.validate import OneOf


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
