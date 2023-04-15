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
    """
    This view function is used to create a new user.
    :return user_id:
    """
    data = get_data_from_request_or_raise_validation_error(SignUpSchema, request.json)
    user, error_data = AuthManager.create_new_user(data)
    if not user:
        return jsonify(error_data), 409
    return jsonify(id=user.id), 201


@auth_router.route("/login", methods=["POST"])
def login():
    """
    This view function is used to get tokens (access and refresh) using valid user credentials.
    :return:
    """
    data = get_data_from_request_or_raise_validation_error(LogInSchema, request.json)
    token, error_msg = AuthManager.get_token(data)
    if error_msg:
        return jsonify(error=error_msg), 403
    return jsonify(token), 200


@auth_router.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    """
    This view function is used to update the access token using a valid refresh token.
    :return:
    """
    token = AuthManager.refresh_access_token()
    return jsonify(token), 200


@auth_router.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile():
    """
    This view function is used to get and update the profile of logged-in user.
    :return:
    """
    if request.method == "GET":
        return jsonify(AuthManager.get_current_user_profile()), 200
    data = get_data_from_request_or_raise_validation_error(UpdateProfile, request.json)
    AuthManager.update_user_profile(data)
    return jsonify(status="success"), 200


@auth_router.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    """
    This view function is used to change the password of logged-in user.
    :return:
    """
    data = get_data_from_request_or_raise_validation_error(UpdatePassword, request.json)
    response, error_msg = AuthManager.update_user_password(data)
    if error_msg:
        return jsonify(error=error_msg), 401
    return jsonify(response), 200


@auth_router.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    """
    This view function is used to log out the user.
    :return:
    """
    return AuthManager.logout()
