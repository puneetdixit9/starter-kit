from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from datetime import datetime
from main.modules.log_event.controller import LogEventController
# from main.modules.user.schema_validator import UpdateProfile
# from main.utils import get_data_from_request_or_raise_validation_error

auth_router = Blueprint("auth", __name__)


class getLogs(Resource):
    # method_decorators = [jwt_required()]

    def get(self, tid: int):
        """
        To get the profile by user_id.
        :param user_id:
        :return:
        """

        # Retrieve the 'from' and 'to' parameters from the request's query string
        from_time = request.args.get('from')
        to_time = request.args.get('to')

        # Convert the string parameters to datetime objects
        from_time = datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
        to_time = datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')

        # Query the logs based on tid and the time range
        logs = LogEventController.get_logs_for_tid_within_time_range(tid, from_time, to_time)
        # Return the logs as a JSON response
        return jsonify(logs)


log_event_namespace = Namespace("logs", description="log Operations")
log_event_namespace.add_resource(getLogs, "/resource_usgae/<int: tid>")
