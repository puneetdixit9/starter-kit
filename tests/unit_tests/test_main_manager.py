from datetime import datetime

from flask_jwt_extended import verify_jwt_in_request

from src.custom_exceptions.exceptions import RecordNotFoundError, UnauthorizedUserError
from src.database import db
from src.database.models.auth import User
from src.database.models.main import Address
from src.managers.main import MainManager
from tests.unit_tests.base_unit_test import BaseUnitTest


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
            address_id = MainManager.add_address(address_data)
            self.assertEqual(2, address_id)
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
        all_addresses = MainManager.get_addresses(self.user)
        self.assertEqual(1, len(all_addresses))
        self.assertEqual("home", all_addresses[0]["type"])

    def test_get_address_by_address_id(self):
        address = MainManager.get_address_by_address_id(self.address.id, self.user)
        self.assertEqual("India", address["country"])

    def test_update_address_success(self):
        with self.app.test_request_context():
            result = MainManager.update_address(self.address.id, {"type": "other"}, self.user)
            self.assertEqual(result, {"msg": "success"})
            self.assertEqual(Address.query.filter_by(id=self.address.id).first().type, "other")

    def test_update_address_record_not_found_error(self):
        with self.app.test_request_context():
            with self.assertRaises(RecordNotFoundError):
                invalid_address_id = -1
                MainManager.update_address(invalid_address_id, {"type": "other"}, self.user)

    def test_update_address_unauthorized_user_error(self):
        with self.app.test_request_context():
            unauthorized_user = User(username="unauthorized_user", email="test2@test.com", password="test")
            db.session.add(unauthorized_user)
            db.session.commit()
            with self.assertRaises(UnauthorizedUserError):
                MainManager.update_address(self.address.id, {"type": "other"}, unauthorized_user)

    def test_delete_address_success(self):
        with self.app.test_request_context():
            result = MainManager.delete_address(self.address.id, self.user)
            self.assertEqual(result, {"msg": "success"})
            self.assertIsNone(Address.query.filter_by(id=self.address.id).first())

    def test_delete_address_record_not_found_error(self):
        with self.app.test_request_context():
            with self.assertRaises(RecordNotFoundError):
                MainManager.delete_address(-1, self.user)

    def test_delete_address_unauthorized_user_error(self):
        with self.app.test_request_context():
            unauthorized_user = User(username="unauthorized_user", email="test2@test.com", password="test")
            db.session.add(unauthorized_user)
            db.session.commit()
            with self.assertRaises(UnauthorizedUserError):
                MainManager.delete_address(self.address.id, unauthorized_user)
