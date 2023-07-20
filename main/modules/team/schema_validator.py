from marshmallow import Schema, fields


class CreateTeam(Schema):
    """
    Required schema to update user profile.
    """

    name = fields.String()
