from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Length, ContainsOnly, OneOf


class SignUpSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=OneOf(["user", "admin"]))
    password = fields.String(required=True, validate=Length(min=8))
    gender = fields.String(validate=ContainsOnly(["male", "female", "other"]))
    address = fields.String()


class LogInSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String(required=True, validate=Length(min=8))

    @validates_schema
    def validate_at_least_one_email_and_username(self, data, **kwargs):
        if not data.get("email") and not data.get("username"):
            raise ValidationError("At least one param is required from ['email', 'username']")


class UpdateProfile(Schema):
    first_name = fields.String()
    last_name = fields.String()
    department = fields.String()
    function = fields.String()
    role = fields.String()
    mobile_number = fields.String()


class UpdatePassword(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=Length(min=8))
