from src.custom_exceptions import RecordNotFoundError, UnauthorizedUserError
from src.database import db
from src.database.models.auth import User
from src.database.models.main import Address
from src.managers.auth import ROLE
from src.utils import update_class_object


class MainManager:
    """
    This class is used to manager all the operations of address.
    """

    @classmethod
    def add_address(cls, address_data: dict):
        """
        This function is used to add new address.
        :param address_data:
        :return int:
        """
        address = Address(**address_data)
        db.session.add(address)
        db.session.commit()
        return address.id

    @classmethod
    def get_addresses(cls, user: User) -> list[dict]:
        """
        This function is used to get the list of addresses of logged-in user. If user is Admin
        then this function will return all addresses.
        :param user:
        :return list[Address]:
        """
        if user.role == ROLE.ADMIN.value:
            addresses = Address.query.all()
        else:
            addresses = Address.query.filter_by(user_id=user.id)
        return [address.as_dict() for address in addresses]

    @classmethod
    def get_address_by_address_id(cls, address_id: int, user: User) -> dict:
        """
        This function is used to get an address by address_id.
        :param address_id:
        :param user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(user, address)
        return address.as_dict()

    @classmethod
    def update_address(cls, address_id: int, updated_address: dict, user: User) -> dict:
        """
        This function is used to update the address. It required a valid address_id.
        :param address_id:
        :param updated_address:
        :param user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(user, address)
        update_class_object(address, updated_address)
        db.session.commit()
        return {"msg": "success"}

    @classmethod
    def delete_address(cls, address_id, user):
        """
        This function is used to delete a address by address_id.
        :param address_id:
        :param user:
        :return dict:
        """
        address = Address.query.filter_by(id=address_id).first()
        cls.required_checks(user, address)
        Address.query.filter_by(id=address_id).delete()
        db.session.commit()
        return {"msg": "success"}

    @classmethod
    def required_checks(cls, user: User, address: Address):
        """
        This function is used to check the required checks and raise a custom exception if any
        check failed. On custom exception server will return a response with defined error msg
        and status code.
        :param user:
        :param address:
        :return:
        """
        if not address:
            raise RecordNotFoundError
        if user.role != ROLE.ADMIN.value and address.user_id != user.id:
            raise UnauthorizedUserError
