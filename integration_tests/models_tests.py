import unittest

from src.database.models.auth import User
from src.database.models.main import Address
from datetime import datetime


class ModelsTests(unittest.TestCase):

    def test_user_model(self):
        user_data = {
            "username": "Puneet",
            "role": "admin",
            "email": "puneet@gmail.com",
            "password": "1234",
        }
        user = User(**user_data)
        self.assertEqual(user.name, "Puneet")
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.email, "puneet@gmail.com")
        self.assertEqual(user.password, "1234")

    def test_address_model(self):
        created_time = datetime.utcnow(),
        address_data = {
            "country": "India",
            "house_no_and_street": "74, ward 4",
            "landmark": "Near govt school",
            "pin_code": 121106,
            "type": "home",
            "created_at": created_time,
            "user_id": 1
        }

        address = Address(**address_data)
    
        self.assertEqual(address.country, "India")
        self.assertEqual(address.house_no_and_street, "74, ward 4")
        self.assertEqual(address.landmark, "Near govt school")
        self.assertEqual(address.pin_code, 121106)
        self.assertEqual(address.type, "home")
        self.assertEqual(address.created_at, created_time)
        self.assertEqual(address.user_id, 1)
