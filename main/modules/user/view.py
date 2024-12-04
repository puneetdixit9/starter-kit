from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

# from main.cache import CacheResource
from main.modules.user.controller import UserController
from main.modules.user.schema_validator import UpdateProfile
from main.utils import get_data_from_request_or_raise_validation_error

auth_router = Blueprint("auth", __name__)


# class Profile(Resource):
#     method_decorators = [jwt_required()]

#     def get(self):
#         """
#         To get the profile of logged-in user.
#         :return:
#         """
#         return jsonify(UserController.get_profile())

#     def put(self):
#         """
#         To update the profile of current user.
#         :return:
#         """
#         data = get_data_from_request_or_raise_validation_error(UpdateProfile, request.json)
#         UserController.update_user_profile(data)
#         return jsonify(msg="success")


class ProfileList(Resource):
    # method_decorators = [jwt_required()]

    def get(self):
        """
        To get all user profiles.
        :return:
        """
        return jsonify(UserController.get_profiles())


class Profiles(Resource):
    # method_decorators = [jwt_required()]

    def get(self, user_id: int):
        """
        To get the profile by user_id.
        :param user_id:
        :return:
        """
        return jsonify(UserController.get_profile(user_id))

    def put(self, user_id: int):
        """
        To update the user profile by user_id
        :param user_id:
        :return:
        """
        data = get_data_from_request_or_raise_validation_error(UpdateProfile, request.json)
        UserController.update_user_profile(data, user_id)
        return jsonify(msg="success")


user_namespace = Namespace("users", description="User Operations")
user_namespace.add_resource(ProfileList, "/profileList")
user_namespace.add_resource(Profiles, "/profiles/<int:user_id>")
