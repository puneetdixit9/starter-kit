from integration_tests.router_base_test import BaseRouterTest
from integration_tests.test_utils import add_address_data


class MainRouterTest(BaseRouterTest):
    def get_headers(self):
        access_token = self.login()["access_token"]

        return {"Authorization": f"Bearer {access_token}"}

    def test_add_address_success(self):
        address = add_address_data()
        response = self.app.post("/address", headers=self.get_headers(), json=address)
        self.assertEqual(response.status_code, 201)

    def test_add_address_failure(self):
        address = add_address_data()

        # Invalid address type
        address["type"] = "test"
        response = self.app.post("/address", headers=self.get_headers(), json=address)
        self.assertEqual(response.status_code, 400)

    def test_get_addresses(self):
        headers = self.get_headers()
        address = add_address_data()

        # Adding addresses two times
        self.app.post("/address", headers=headers, json=address)
        address["type"] = "other"
        self.app.post("/address", headers=headers, json=address)

        response = self.app.get("/addresses", headers=headers, json=address)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_update_address(self):
        headers = self.get_headers()

        address = add_address_data()
        response = self.app.post("/address", headers=headers, json=address)
        self.assertEqual(response.status_code, 201)
        address["address_id"] = response.json["address_id"]
        address["type"] = "other"
        response = self.app.put("/address", headers=headers, json=address)
        self.assertEqual(response.status_code, 200)

    def test_delete_address_success(self):
        headers = self.get_headers()

        address = add_address_data()
        response = self.app.post("/address", headers=headers, json=address)
        self.assertEqual(response.status_code, 201)

        response = self.app.delete(f"/address/{response.json['address_id']}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_address_failure(self):
        address_id = 10  # Invalid address_id
        response = self.app.delete(f"/address/{address_id}", headers=self.get_headers())
        self.assertEqual(response.status_code, 404)
