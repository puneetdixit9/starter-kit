from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from main.modules.auth.model import AuthUser


def allowed_roles(roles: list):
    """
    This decorator function is used for verifying allowed roles using jwt token and user role.
    :param roles:
    :return:
    """

    def role_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            auth_user = AuthUser.query.filter_by(id=identity["user_id"]).first()
            if not auth_user:
                return jsonify({"error": "User Not Found !!"}), 403
            elif auth_user.role not in roles:
                return jsonify({"error": "Unauthorized User!!"}), 401
            return f(*args, **kwargs)

        return decorated

    return role_required
