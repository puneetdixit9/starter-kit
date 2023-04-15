from src.managers.auth import AuthManager
from tests.integration_tests.router_base_test import BaseRouterTest
from tests.integration_tests.test_utils import add_address_data


class MainRouterTest(BaseRouterTest):
    def add_fixtures(self):
        admin = {"username": "testadmin", "email": "testadmin@gmail.com", "password": "test_password", "role": "admin"}
        admin, _ = AuthManager.create_new_user(admin)
        self.admin = admin
        self.admin_headers = self.get_headers({"email": "testadmin@gmail.com", "password": "test_password"})
        admin = {"username": "testuser", "email": "testuser@gmail.com", "password": "test_password", "role": "user"}
        self.user, _ = AuthManager.create_new_user(admin)
        self.user_headers = self.get_headers({"email": "testuser@gmail.com", "password": "test_password"})

    def get_headers(self, login_data=None):
        access_token = self.login(login_data)["access_token"]
        return {"Authorization": f"Bearer {access_token}"}

    def test_add_address_success(self):
        address = add_address_data()
        response = self.client.post("/addresses", headers=self.get_headers(), json=address)
        self.assertEqual(response.status_code, 201)

    def test_add_address_failure(self):
        address = add_address_data()

        # Invalid address type
        address["type"] = "test"
        response = self.client.post("/addresses", headers=self.get_headers(), json=address)
        self.assertEqual(response.status_code, 400)

    def test_get_addresses(self):
        headers = self.get_headers()
        address = add_address_data()

        # Adding addresses two times
        self.client.post("/addresses", headers=headers, json=address)
        address["type"] = "other"
        response = self.client.post("/addresses", headers=headers, json=address)
        address_id = response.json["id"]
        response = self.client.get("/addresses", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        response = self.client.get(f"/addresses/{address_id}", headers=headers)
        self.assertEqual(response.json["id"], address_id)

    def test_unauthorized_user_error(self):
        address = add_address_data()
        response = self.client.post("/addresses", headers=self.user_headers, json=address)
        address_id = response.json["id"]
        unauthorized_user_headers = self.get_headers()
        response = self.client.get(f"/addresses/{address_id}", headers=unauthorized_user_headers)
        self.assertEqual(response.status_code, 401)

    def test_get_address_using_admin(self):
        response = self.client.get("/addresses", headers=self.admin_headers)
        self.assertEqual(0, len(response.json))

    def test_update_address(self):
        headers = self.get_headers()

        address = add_address_data()
        response = self.client.post("/addresses", headers=headers, json=address)
        self.assertEqual(response.status_code, 201)
        address["type"] = "other"
        response = self.client.put(f"/addresses/{response.json['id']}", headers=headers, json=address)
        self.assertEqual(response.status_code, 200)

    def test_delete_address_success(self):
        headers = self.get_headers()

        address = add_address_data()
        response = self.client.post("/addresses", headers=headers, json=address)
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(f"/addresses/{response.json['id']}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_address_failure(self):
        address_id = 10  # Invalid address_id
        response = self.client.delete(f"/addresses/{address_id}", headers=self.get_headers())
        self.assertEqual(response.status_code, 404)
