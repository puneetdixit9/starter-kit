from src.schema_validators.auth import SignUpSchema, LogInSchema, UpdateProfile, UpdatePassword
from flask import Blueprint

from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required,
)

from src.managers import AuthManager
from src.managers import jwt

auth_router = Blueprint('auth', __name__)


@auth_router.route('/signup', methods=["POST"])
def signup():
    data = request.json
    schema = SignUpSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user, error_data = AuthManager.create_new_user(data)
    if not user:
        return jsonify(error_data), 409
    return jsonify(id=user.id), 201


@auth_router.route('/login', methods=['POST'])
def login():
    data = request.json
    schema = LogInSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    token, status_code = AuthManager.get_token(data)
    return jsonify(token), status_code


@auth_router.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    return AuthManager.refersh_access_token()


@auth_router.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    if request.method == "GET":
        return jsonify(AuthManager.get_current_user_profile()), 200
    data = request.json
    schema = UpdateProfile()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    AuthManager.update_user_profile(data)
    return jsonify(status="success"), 200


@auth_router.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.json
    schema = UpdatePassword()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    return AuthManager.update_user_password(data)


@auth_router.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    return AuthManager.logout()
