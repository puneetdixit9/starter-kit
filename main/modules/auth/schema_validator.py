from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length, OneOf


class SignUpSchema(Schema):
    """
    In this schema we defined the required json for signup any user.
    """

    first_name = fields.String()
    last_name = fields.String()
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=OneOf(["user", "admin"]))
    password = fields.String(required=True, validate=Length(min=8))


class LogInSchema(Schema):
    """
    In this schema we defined the required json to log in any user.
    """

    username = fields.String()
    email = fields.Email()
    password = fields.String(required=True, validate=Length(min=8))

    @validates_schema
    def validate_at_least_one_email_and_username(self, data, **kwargs):
        if not data.get("email") and not data.get("username"):
            raise ValidationError("At least one param is required from ['email', 'username']")


class UpdatePassword(Schema):
    """
    Required schema to update the password
    """

    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=Length(min=8))
