from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from main.modules.auth.controller import AuthUserController
from main.modules.auth.schema_validator import LogInSchema, SignUpSchema, UpdatePassword
from main.utils import get_data_from_request_or_raise_validation_error


class SignUp(Resource):
    def post(self):
        """
        This view function is used to create a new user.
        :return user_id:
        """
        data = get_data_from_request_or_raise_validation_error(SignUpSchema, request.json)
        user, error_data = AuthUserController.create_new_user(data)
        if not user:
            return make_response(jsonify(error_data), 409)
        return make_response(jsonify(id=user.id), 201)


class Login(Resource):
    def post(self):
        """
        This view function is used to get tokens (access and refresh) using valid user credentials.
        :return:
        """
        data = get_data_from_request_or_raise_validation_error(LogInSchema, request.json)
        token, error_msg = AuthUserController.get_token(data)
        if error_msg:
            return make_response(jsonify(error=error_msg), 403)
        return make_response(jsonify(token), 200)


class Refresh(Resource):
    method_decorators = [jwt_required(refresh=True)]

    def get(self):
        """
        This view function is used to update the access token using a valid refresh token.
        :return:
        """
        return jsonify(AuthUserController.refresh_access_token())


class ChangePassword(Resource):
    method_decorators = [jwt_required()]

    def put(self):
        """
        This view function is used to change the password of logged-in user.
        :return:
        """
        data = get_data_from_request_or_raise_validation_error(UpdatePassword, request.json)
        response, error_msg = AuthUserController.update_user_password(data)
        if error_msg:
            return make_response(jsonify(error=error_msg), 401)
        return jsonify(response)


class Logout(Resource):
    method_decorators = [jwt_required(verify_type=False)]

    def delete(self):
        """
        This view function is used to log out the user.
        :return:
        """
        return jsonify(AuthUserController.logout())


auth_namespace = Namespace("auth", description="Auth Operations")
auth_namespace.add_resource(SignUp, "/signup")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(ChangePassword, "/change_password")
auth_namespace.add_resource(Logout, "/logout")
