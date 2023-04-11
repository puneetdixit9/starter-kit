from flask import Blueprint
from src.managers import ROLE
from flask import request, jsonify

from src.decorators.user_role import allowed_roles
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from src.schema_validators.main import (
    AddAddressSchema,
    UpdateAddressSchema
)
from src.managers import MainManager
from src.managers import AuthManager


main_router = Blueprint('main', __name__)


@main_router.route('/', methods=['GET'])
def server_status():
    return jsonify({"message": "server is up"}), 200


@main_router.route('/address', methods=["POST"])
@jwt_required()
@allowed_roles([ROLE.USER.value])  # Allowed for User role type.
def add_address():
    data = request.json
    schema = AddAddressSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    return MainManager.add_address(data)


@main_router.route('/addresses', methods=["GET"])
@jwt_required()
@allowed_roles([ROLE.ADMIN.value, ROLE.USER.value])  # Allowed for Admin and User role type.
def get_addresses():
    user = AuthManager.get_current_user()
    user_id = request.args.get("id")
    if user.role == ROLE.ADMIN.value:
        if not user_id:
            data = MainManager.get_all_addresses()
    else:
        user_id = user.id
        data = MainManager.get_addresses_by_user_id(user_id)
    return jsonify(data), 200


@main_router.route('/address', methods=['PUT'])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def update_address():
    data = request.json
    schema = UpdateAddressSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    return MainManager.update_address(data, AuthManager.get_current_user())


@main_router.route('/address/<address_id>', methods=['DELETE'])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def delete_address(address_id):
    return MainManager.delete_address(address_id, AuthManager.get_current_user())
