from flask_jwt_extended import get_jwt_identity

from src.database import db
from src.database.models.main import Address
from src.utils import update_class_object


class MainManager:
    @classmethod
    def add_address(cls, address_data):
        identity = get_jwt_identity()
        user_id = identity["user_id"]
        address_data.update({"user_id": user_id})
        address = Address(**address_data)
        db.session.add(address)
        db.session.commit()

        return {"address_id": address.id, "status": "success"}

    @classmethod
    def get_all_addresses(cls):
        addresses = Address.query.all()
        return [address.as_dict() for address in addresses]

    @classmethod
    def get_addresses_by_user_id(cls, user_id):
        addresses = Address.query.filter_by(user_id=user_id)
        return [address.as_dict() for address in addresses]

    @classmethod
    def get_address_by_address_id(cls, address_id):
        return Address.query.filter_by(id=address_id).first()

    @classmethod
    def update_address(cls, updated_address, current_user):
        address = cls.get_address_by_address_id(updated_address["address_id"])
        if not address:
            return {"error": "address_id not found"}, 404

        if address.user_id != current_user.id:
            return {"error": "Unauthorized user"}, 401

        update_class_object(address, updated_address)

        db.session.commit()
        return {"msg": "success"}, 200

    @classmethod
    def delete_address(cls, address_id, current_user):
        address = cls.get_address_by_address_id(address_id)
        if not address:
            return {"error": "address_id not found"}, 404

        if address.user_id != current_user.id:
            return {"error": "Unauthorized user"}, 401

        Address.query.filter_by(id=address_id).delete()
        db.session.commit()
        return {"msg": "success"}, 200
