from marshmallow import Schema, fields


class UpdateProfile(Schema):
    """
    Required schema to update user profile.
    """

    first_name = fields.String()
    last_name = fields.String()
    department = fields.String()
    function = fields.String()
    role = fields.String()
