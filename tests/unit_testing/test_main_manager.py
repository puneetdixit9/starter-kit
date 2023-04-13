from datetime import datetime

from flask_jwt_extended import verify_jwt_in_request

from src.database import db
from src.database.models.auth import User
from src.database.models.main import Address
from src.managers.main import MainManager
from tests.unit_testing.base_unit_test import BaseUnitTest


class TestAuthManager(BaseUnitTest):
    def add_fixtures(self):
        user_data = {
            "username": "test1",
            "email": "test1@email.com",
            "password": "testpassword",
            "role": "user",
        }
        user = User(**user_data)
        self.user = user
        db.session.add(user)
        db.session.commit()
        address_data = {
            "type": "home",
            "house_no_and_street": "1 ABC",
            "landmark": "xyz",
            "country": "India",
            "pin_code": "123456",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "user_id": user.id,
        }
        address = Address(**address_data)
        self.address = address
        db.session.add(address)
        db.session.commit()

    def test_add_address(self):
        user, headers = self.get_user_and_headers()
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            address_data = {
                "type": "home",
                "house_no_and_street": "1 ABC",
                "landmark": "xyz",
                "country": "India",
                "pin_code": "123456",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "user_id": user.id,
            }
            response_data = MainManager.add_address(address_data)
            self.assertIn("address_id", response_data)
            address_id = response_data["address_id"]
            address = Address.query.filter_by(id=address_id).first()
            self.assertIsNotNone(address)
            self.assertEqual(address.user_id, user.id)
            self.assertEqual(address.type, address_data["type"])
            self.assertEqual(address.house_no_and_street, address_data["house_no_and_street"])
            self.assertEqual(address.landmark, address_data["landmark"])
            self.assertEqual(address.country, address_data["country"])
            self.assertEqual(address.pin_code, address_data["pin_code"])
            self.assertEqual(address.created_at, address_data["created_at"])
            self.assertEqual(address.updated_at, address_data["updated_at"])

    def test_get_all_address(self):
        all_addresses = MainManager.get_all_addresses()
        self.assertEqual(1, len(all_addresses))
        self.assertEqual("home", all_addresses[0]["type"])

    def test_get_address_by_user_id(self):
        all_addresses = MainManager.get_addresses_by_user_id(self.user.id)
        self.assertEqual(1, len(all_addresses))
        self.assertEqual("home", all_addresses[0]["type"])

    def test_get_address_by_address_id(self):
        address = MainManager.get_address_by_address_id(self.address.id)
        self.assertEqual("India", address.country)

    def test_update_address(self):
        invalid_user, headers = self.get_user_and_headers()
        updated_address = {"type": "work", "address_id": 999}  # invalid id

        response = MainManager.update_address(updated_address, invalid_user)
        self.assertEqual(response[0], {"error": "address_id not found"})
        self.assertEqual(response[1], 404)

        updated_address["address_id"] = self.address.id
        response = MainManager.update_address(updated_address, invalid_user)
        self.assertEqual(response[0], {"error": "Unauthorized user"})
        self.assertEqual(response[1], 401)

        response = MainManager.update_address(updated_address, self.user)
        self.assertEqual(response[0], {"msg": "success"})
        self.assertEqual(response[1], 200)

    def test_delete_address(self):
        invalid_user, headers = self.get_user_and_headers()

        response = MainManager.delete_address(999, invalid_user)  # invalid address_id
        self.assertEqual(response[0], {"error": "address_id not found"})
        self.assertEqual(response[1], 404)

        response = MainManager.delete_address(self.address.id, invalid_user)
        self.assertEqual(response[0], {"error": "Unauthorized user"})
        self.assertEqual(response[1], 401)

        response = MainManager.delete_address(self.address.id, self.user)
        self.assertEqual(response[0], {"msg": "success"})
        self.assertEqual(response[1], 200)
