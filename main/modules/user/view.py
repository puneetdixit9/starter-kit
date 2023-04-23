from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from main.modules.user.controller import UserController
from main.modules.user.schema_validator import UpdateProfile
from main.utils import get_data_from_request_or_raise_validation_error

auth_router = Blueprint("auth", __name__)


class Profile(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This view function is used to get the profile of logged-in user.
        :return:
        """
        return jsonify(UserController.get_current_user_profile())

    def put(self):
        """
        This view function is used to update the profile of current user.
        :return:
        """
        data = get_data_from_request_or_raise_validation_error(UpdateProfile, request.json)
        UserController.update_user_profile(data)
        return make_response(jsonify(status="success"), 200)


profile_namespace = Namespace("users", description="User Operations")
profile_namespace.add_resource(Profile, "/profile")
