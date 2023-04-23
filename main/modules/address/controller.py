from main.custom_exceptions import RecordNotFoundError, UnauthorizedUserError
from main.modules.address.model import Address
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from src.managers.auth import ROLE


class AddressController:
    """
    This is the controller class which is used to handle all the logical and CURD operations.
    """

    @classmethod
    def add_address(cls, address_data: dict):
        """
        This function is used to add new address.
        :param address_data:
        :return int:
        """
        address = Address.create(address_data)
        return address.id

    @classmethod
    def get_addresses(cls, auth_user: AuthUser) -> list[dict]:
        """
        This function is used to get the list of addresses of logged-in auth_user. If auth_user is Admin
        then this function will return all addresses.
        :param auth_user:
        :return list[Address]:
        """
        if auth_user.role == ROLE.ADMIN.value:
            addresses = Address.query.all()
        else:
            addresses = Address.query.filter_by(user_id=auth_user.id)
        return [address.serialize() for address in addresses]

    @classmethod
    def get_address_by_address_id(cls, address_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an address by address_id.
        :param address_id:
        :param auth_user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(auth_user, address)
        return address.serialize()

    @classmethod
    def update_address(cls, address_id: int, updated_address: dict, auth_user: AuthUser) -> dict:
        """
        This function is used to update the address. It required a valid address_id.
        :param address_id:
        :param updated_address:
        :param auth_user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(auth_user, address)
        address.update(updated_address)
        return {"msg": "success"}

    @classmethod
    def delete_address(cls, address_id, auth_user):
        """
        This function is used to delete a address by address_id.
        :param address_id:
        :param auth_user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(auth_user, address)
        Address.delete({"id": address_id})
        return {"msg": "success"}

    @classmethod
    def required_checks(cls, auth_user: AuthUser, address: Address):
        """
        This function is used to check the required checks and raise a custom exception if any
        check failed. On custom exception server will return a response with defined error msg
        and status code.
        :param auth_user:
        :param address:
        :return:
        """
        if not address:
            raise RecordNotFoundError
        if auth_user.role != AuthUserController.ROLES.ADMIN.value and address.user_id != auth_user.id:
            raise UnauthorizedUserError
