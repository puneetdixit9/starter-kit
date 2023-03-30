from datetime import datetime
from functools import wraps
from flask import jsonify
from project.models.user_models import User
from flask_jwt_extended import get_jwt_identity


def get_user():
    identity = get_jwt_identity()
    return User.query.filter_by(id=identity['user_id']).first()


def create_address_response(data):
    return [{
        "address_id": record.id,
        "user_id": record.user_id,
        "submitter_name": User.query.filter_by(id=record.user_id).first().name,
        "country": record.country,
        "house_no_and_street": record.house_no_and_street,
        "landmark": record.landmark,
        "type": record.type,
        "pin_code": record.pin_code,
        "created_at": record.created_at,
        "updated_at": record.updated_at
    } for record in data]


# decorator for verifying the JWT
def allowed_roles(roles):
    def role_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            user = User.query.filter_by(id=identity['user_id']).first()
            if not user:
                return jsonify({'message': 'User Not Found !!'}), 403
            elif user.role not in roles:
                return jsonify({'message': 'Unauthorized User!!'}), 401
            return f(*args, **kwargs)

        return decorated

    return role_required


def update_address_with_new_values(old_address, new_address):
    if "type" in new_address:
        old_address.type = new_address["type"]

    if "house_no_and_street" in new_address:
        old_address.house_no_and_street = new_address["house_no_and_street"]

    if "landmark" in new_address:
        old_address.landmark = new_address["landmark"]

    if "country" in new_address:
        old_address.country = new_address["country"]

    if "pin_code" in new_address:
        old_address.pin_code = new_address["pin_code"]

    old_address.updated_at = datetime.utcnow()
