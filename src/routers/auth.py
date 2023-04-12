from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.managers.auth import AuthManager
from src.schema_validators.auth import (
    LogInSchema,
    SignUpSchema,
    UpdatePassword,
    UpdateProfile,
)
from src.utils import get_data_from_request_or_raise_validation_error

auth_router = Blueprint("auth", __name__)


@auth_router.route("/signup", methods=["POST"])
def signup():
    data = get_data_from_request_or_raise_validation_error(SignUpSchema, request.json)
    user, error_data = AuthManager.create_new_user(data)
    if not user:
        return jsonify(error_data), 409
    return jsonify(id=user.id), 201


@auth_router.route("/login", methods=["POST"])
def login():
    data = get_data_from_request_or_raise_validation_error(LogInSchema, request.json)
    token, status_code = AuthManager.get_token(data)
    return jsonify(token), status_code


@auth_router.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    return AuthManager.refresh_access_token()


@auth_router.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile():
    if request.method == "GET":
        return jsonify(AuthManager.get_current_user_profile()), 200
    data = get_data_from_request_or_raise_validation_error(UpdateProfile, request.json)
    AuthManager.update_user_profile(data)
    return jsonify(status="success"), 200


@auth_router.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    data = get_data_from_request_or_raise_validation_error(UpdatePassword, request.json)
    return AuthManager.update_user_password(data)


@auth_router.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    return AuthManager.logout()
