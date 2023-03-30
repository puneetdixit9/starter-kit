from marshmallow import Schema, fields, ValidationError
import enum


class AddressType(enum.Enum):
    HOME = "home"
    WORK = "work"
    OTHER = "other"


class AddressTypeField(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        options = [e.value for e in AddressType]
        address_types = {val: val for val in options}
        try:
            return address_types[value]
        except KeyError as err:
            raise ValidationError(f'Value must be one of: {options}')


class AddAddressSchema(Schema):
    type = AddressTypeField(required=True)
    house_no_and_street = fields.String(required=True)
    landmark = fields.String(required=False)
    country = fields.String(required=True)
    pin_code = fields.Integer(required=True)


class UpdateAddressSchema(Schema):
    address_id = fields.Integer(required=True)
    type = AddressTypeField(required=False)
    house_no_and_street = fields.String(required=False)
    landmark = fields.String(required=False)
    country = fields.String(required=False)
    pin_code = fields.Integer(required=False)
