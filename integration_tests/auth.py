from integration_tests.test_utils import get_signup_data, get_login_data, get_update_password_data
from integration_tests.router_base_test import BaseRouterTest


class AuthRouterTest(BaseRouterTest):

    def test_signup_success(self):
        signup_data = get_signup_data()
        response = self.app.post("/signup", json=signup_data)
        self.assertEqual(response.status_code, 201)

    def test_signup_minimum_password_length(self):
        signup_data = get_signup_data()
        signup_data['password'] = "123"
        response = self.app.post("/signup", json=signup_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["password"][0], "Shorter than minimum length 8.")

    def test_signup_user_already_exists(self):
        signup_data = get_signup_data()
        response = self.app.post("/signup", json=signup_data)
        self.assertEqual(response.status_code, 201)

        # again signup with same email
        response = self.app.post("/signup", json=signup_data)
        self.assertEqual(response.status_code, 409)  # user already exists
        self.assertEqual("user already exists with provided username", response.json["error"])

    def test_login_success(self):
        self.signup()
        login_data = get_login_data()
        response = self.app.post("/login", json=login_data)
        self.assertEqual(response.status_code, 200)

    def test_login_failure_with_wrong_email(self):
        self.signup()
        login_data = get_login_data()
        login_data["email"] = "wrongemail@gmail.com"
        response = self.app.post("/login", json=login_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual('user not found with wrongemail@gmail.com', response.json["error"])

    def test_change_password_success(self):
        access_token = self.login()["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        update_password_data = get_update_password_data()
        response = self.app.put("/change_password", headers=headers, json=update_password_data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_without_access_token(self):
        self.login()
        update_password_data = get_update_password_data()
        headers = {}
        response = self.app.put("/change_password", headers=headers, json=update_password_data)
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_get_access_token_from_refresh_token(self):
        refresh_token = self.login()["refresh_token"]
        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }
        response = self.app.get('/refresh', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        token = self.login()
        headers = {
            "Authorization": f"Bearer {token['access_token']}"
        }
        response = self.app.delete('/logout', headers=headers)
        self.assertEqual(response.status_code, 200)

        headers = {
            "Authorization": f"Bearer {token['refresh_token']}"
        }
        response = self.app.delete('/logout', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_revoked_token(self):
        token = self.login()
        headers = {
            "Authorization": f"Bearer {token['access_token']}"
        }
        response = self.app.delete('/logout', headers=headers)  # logout access token
        self.assertEqual(response.status_code, 200)

        # trying to change password with revoked token
        update_password_data = get_update_password_data()
        response = self.app.put("/change_password", headers=headers, json=update_password_data)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], 'Token has been revoked')

        headers["Authorization"] = f"Bearer {token['refresh_token']}"
        response = self.app.delete('/logout', headers=headers)  # logout refresh token
        self.assertEqual(response.status_code, 200)

        #  trying to get access token using revoked refresh token
        response = self.app.get('/refresh', headers=headers)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], 'Token has been revoked')

