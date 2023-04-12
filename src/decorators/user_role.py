from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from src.database.models.auth import User


# decorator for verifying the JWT
def allowed_roles(roles):
    def role_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            user = User.query.filter_by(id=identity["user_id"]).first()
            if not user:
                return jsonify({"error": "User Not Found !!"}), 403
            elif user.role not in roles:
                return jsonify({"error": "Unauthorized User!!"}), 401
            return f(*args, **kwargs)

        return decorated

    return role_required
