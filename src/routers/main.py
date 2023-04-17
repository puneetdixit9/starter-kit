from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from src.managers.auth import AuthManager
from src.managers.main import MainManager
from src.schema_validators.main import AddAddressSchema, UpdateAddressSchema
from src.utils import get_data_from_request_or_raise_validation_error


class AddressApi(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This function is used to get the list of addresses.
        :return:
        """
        user = AuthManager.get_current_user()
        response = MainManager.get_addresses(user)
        return jsonify(response)

    def post(self):
        """
        This function is used to add new address to the database.
        :return:
        """
        user = AuthManager.get_current_user()
        data = get_data_from_request_or_raise_validation_error(AddAddressSchema, request.json)
        data.update({"user_id": user.id})
        address_id = MainManager.add_address(data)
        response = make_response(
            jsonify({"message": "Address added", "location": f"/addresses/{address_id}", "id": address_id}), 201
        )
        response.headers["Location"] = f"/addresses/{address_id}"
        return response


class AddressApi2(Resource):
    method_decorators = [jwt_required()]

    def get(self, address_id):
        """
        This function is used to get the particular address by address_id
        :param address_id:
        :return:
        """
        user = AuthManager.get_current_user()
        response = MainManager.get_address_by_address_id(address_id, user)
        return jsonify(response)

    def put(self, address_id):
        """
        This function is used to update the address by address_id
        :param address_id:
        :return:
        """
        user = AuthManager.get_current_user()
        data = get_data_from_request_or_raise_validation_error(UpdateAddressSchema, request.json)
        response = MainManager.update_address(address_id, data, user)
        return jsonify(response)

    def delete(self, address_id):
        """
        This function is used to delete the address by address_id.
        :param address_id:
        :return:
        """
        user = AuthManager.get_current_user()
        response = MainManager.delete_address(address_id, user)
        return jsonify(response)
