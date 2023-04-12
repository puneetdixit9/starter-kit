from marshmallow import Schema, fields, validate


class AddAddressSchema(Schema):
    type = fields.String(validate=validate.OneOf(["home", "work", "other"]), required=True)
    house_no_and_street = fields.String(required=True)
    landmark = fields.String(required=False)
    country = fields.String(required=True)

    pin_code = fields.Integer(required=True)


class UpdateAddressSchema(Schema):
    address_id = fields.Integer(required=True)
    type = fields.String(validate=validate.OneOf(["home", "work", "other"]), required=False)
    house_no_and_street = fields.String(required=False)
    landmark = fields.String(required=False)
    country = fields.String(required=False)
    pin_code = fields.Integer(required=False)
