from src.database import db
from src.database.models.auth import User
from src.database.models.main import Address
from src.utils import update_class_object
from tests.unit_tests.base_unit_test import BaseUnitTest


class ModelsTests(BaseUnitTest):
    def add_fixtures(self):
        user_data = {
            "username": "test",
            "role": "admin",
            "email": "test@gmail.com",
            "password": "1234",
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        self.user = user

        address_data = {
            "country": "test",
            "house_no_and_street": "74, ward 4",
            "landmark": "test",
            "pin_code": 121106,
            "type": "home",
            "user_id": self.user.id,
        }
        address = Address(**address_data)
        db.session.add(address)
        db.session.commit()
        self.address = address

    def test_create_user(self):
        user_data = {
            "username": "Puneet",
            "role": "admin",
            "email": "puneet@gmail.com",
            "password": "1234",
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, "Puneet")
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.email, "puneet@gmail.com")
        self.assertEqual(user.password, "1234")

    def test_get_user(self):
        user = User.query.filter_by(id=self.user.id).first()  # getting user from db
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.user.username)
        self.assertIsNone(user.updated_at)
        self.assertIsNotNone(user.created_at)
        user = user.as_dict()  # converting user into dict form
        self.assertEqual(user["email"], self.user.email)

    def test_update_user(self):
        user = User.query.filter_by(id=self.user.id).first()
        self.assertIsNone(user.updated_at)
        update_class_object(user, {"username": "test", "password": "test"})
        db.session.commit()
        self.assertEqual(user.username, "test")
        self.assertEqual(user.password, "test")
        self.assertEqual(user.role, self.user.role)
        self.assertIsNotNone(user.updated_at)

    def test_delete_user(self):
        self.assertIsNotNone(self.user)
        User.query.filter_by(id=self.user.id).delete()
        user = User.query.filter_by(id=self.user.id).first()
        self.assertIsNone(user)

    def test_create_address(self):
        address_data = {
            "country": "India",
            "house_no_and_street": "74, ward 4",
            "landmark": "Near govt school",
            "pin_code": 121106,
            "type": "home",
            "user_id": 1,
        }

        address = Address(**address_data)
        db.session.add(address)
        db.session.commit()
        self.assertEqual(address.country, "India")
        self.assertEqual(address.house_no_and_street, "74, ward 4")
        self.assertEqual(address.landmark, "Near govt school")
        self.assertEqual(address.pin_code, str(121106))
        self.assertEqual(address.type, "home")
        self.assertEqual(address.user_id, 1)

    def test_get_address(self):
        address = Address.query.filter_by(id=self.address.id).first()
        self.assertIsNotNone(address)
        self.assertEqual(address.type, self.address.type)
        self.assertEqual(address.country, self.address.country)

        address = address.as_dict()
        self.assertEqual(address["landmark"], self.address.landmark)

    def test_update_address(self):
        address = Address.query.filter_by(id=self.address.id).first()
        self.assertIsNotNone(address)
        self.assertIsNone(address.updated_at)
        self.assertEqual(address.landmark, self.address.landmark)
        update_class_object(address, {"landmark": "test", "country": "test"})
        db.session.commit()
        self.assertEqual(address.landmark, "test")
        self.assertEqual(address.country, "test")

    def test_delete_address(self):
        self.assertIsNotNone(self.address)
        Address.query.filter_by(id=self.address.id).delete()
        address = Address.query.filter_by(id=self.address.id).first()
        self.assertIsNone(address)
