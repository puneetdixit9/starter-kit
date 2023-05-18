from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace

from main.cache import CacheResource
from main.modules.address.controller import AddressController
from main.modules.address.schema_validator import AddAddressSchema, UpdateAddressSchema
from main.modules.auth.controller import AuthUserController
from main.utils import get_data_from_request_or_raise_validation_error


class AddressApi(CacheResource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This function is used to get the list of addresses.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = AddressController.get_addresses(auth_user)
        return jsonify(response)

    def post(self):
        """
        This function is used to add new address to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(AddAddressSchema, request.json)
        data.update({"user_id": auth_user.id})
        address_id = AddressController.add_address(data)
        response = make_response(
            jsonify({"message": "Address added", "location": f"/addresses/{address_id}", "id": address_id}), 201
        )
        response.headers["Location"] = f"/addresses/{address_id}"
        return response


class AddressApi2(CacheResource):
    method_decorators = [jwt_required()]

    def get(self, address_id: int):
        """
        This function is used to get the particular address by address_id
        :param address_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = AddressController.get_address_by_address_id(address_id, auth_user)
        return jsonify(response)

    def put(self, address_id: int):
        """
        This function is used to update the address by address_id
        :param address_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(UpdateAddressSchema, request.json)
        response = AddressController.update_address(address_id, data, auth_user)
        return jsonify(response)

    def delete(self, address_id: int):
        """
        This function is used to delete the address by address_id.
        :param address_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = AddressController.delete_address(address_id, auth_user)
        return jsonify(response)


address_namespace = Namespace("addresses", description="Address Operations")
address_namespace.add_resource(AddressApi, "")
address_namespace.add_resource(AddressApi2, "/<int:address_id>")
