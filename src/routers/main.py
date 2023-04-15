from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.decorators.user_role import allowed_roles
from src.managers.auth import ROLE, AuthManager
from src.managers.main import MainManager
from src.schema_validators.main import AddAddressSchema, UpdateAddressSchema
from src.utils import get_data_from_request_or_raise_validation_error

main_router = Blueprint("main", __name__)


@main_router.route("/addresses/<address_id>", methods=["GET", "PUT", "DELETE"])
@main_router.route("/addresses", methods=["POST", "GET"])
@jwt_required()
@allowed_roles([ROLE.ADMIN.value, ROLE.USER.value])
def addresses(address_id: int = None):
    """
    This view function is used to handle all CURD operation of address.
    :param address_id:
    :return:
    """
    user = AuthManager.get_current_user()
    if request.method == "GET":
        if not address_id:
            response = MainManager.get_addresses(user)
        else:
            response = MainManager.get_address_by_address_id(address_id, user)
        return jsonify(response)

    elif request.method == "POST":
        data = get_data_from_request_or_raise_validation_error(AddAddressSchema, request.json)
        data.update({"user_id": user.id})
        response = MainManager.add_address(data)
        return jsonify(id=response), 201

    elif request.method == "PUT":
        data = get_data_from_request_or_raise_validation_error(UpdateAddressSchema, request.json)
        response = MainManager.update_address(address_id, data, user)
        return jsonify(response)

    else:
        response = MainManager.delete_address(address_id, user)
        return jsonify(response)
