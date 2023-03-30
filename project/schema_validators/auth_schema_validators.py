from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length
import enum


class ROLE(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class RoleField(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        options = [e.value for e in ROLE]
        roles = {val: val for val in options}
        try:
            return roles[value]
        except KeyError as err:
            raise ValidationError(f'Value must be one of: {options}')


class SignUpSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8))
    role = RoleField(required=True)


class LogInSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UpdatePassword(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=Length(min=8))

