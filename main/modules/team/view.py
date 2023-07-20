from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

# from main.cache import CacheResource
from main.modules.team.controller import TeamController
from main.modules.team.schema_validator import CreateTeam
from main.utils import get_data_from_request_or_raise_validation_error

import uuid


auth_router = Blueprint("auth", __name__)


class getTeam(Resource):
    method_decorators = [jwt_required()]

    def get(self, tid):
        """
        To get the profile of logged-in user.
        :return:
        """
        return jsonify(TeamController.get_team(tid))


class createTeam(Resource):
    method_decorators = [jwt_required()]

    def post(self):

        data = get_data_from_request_or_raise_validation_error(CreateTeam , request.json)
        # print(data)

        # Generate a UUID
        generated_uuid = uuid.uuid4()
        # Remove dashes from the UUID and return the first 16 characters
        uuid_without_special_chars = str(generated_uuid).replace('-', '')[:16]
        data['tid'] = uuid_without_special_chars
        TeamController.create_team_profile(data)
        return jsonify(msg="success")


team_namespace = Namespace("team", description="Team Operations")
team_namespace.add_resource(getTeam, "/getTeam/<string:tid>")
team_namespace.add_resource(createTeam , "/create")
