from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.decorators.user_role import allowed_roles
from src.managers.auth import ROLE, AuthManager
from src.managers.main import MainManager
from src.schema_validators.main import AddAddressSchema, UpdateAddressSchema
from src.utils import get_data_from_request_or_raise_validation_error

main_router = Blueprint("main", __name__)


@main_router.route("/", methods=["GET"])
def server_status():
    return jsonify({"message": "server is up"}), 200


@main_router.route("/address", methods=["POST"])
@jwt_required()
@allowed_roles([ROLE.USER.value])  # Allowed for User role type.
def add_address():
    data = get_data_from_request_or_raise_validation_error(AddAddressSchema, request.json)
    return MainManager.add_address(data)


@main_router.route("/addresses", methods=["GET"])
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


@main_router.route("/address", methods=["PUT"])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def update_address():
    data = get_data_from_request_or_raise_validation_error(UpdateAddressSchema, request.json)
    return MainManager.update_address(data, AuthManager.get_current_user())


@main_router.route("/address/<address_id>", methods=["DELETE"])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def delete_address(address_id):
    return MainManager.delete_address(address_id, AuthManager.get_current_user())
