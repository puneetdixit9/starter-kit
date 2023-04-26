from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.decorators.user_role import allowed_roles
from tests.unit_tests.base_unit_test import BaseUnitTest


class TestAllowedRolesDecorator(BaseUnitTest):
    @allowed_roles(["user"])
    def user_view(self):
        return "success"

    @allowed_roles(["admin"])
    def admin_view(self):
        return "success"

    def test_allowed_roles_decorator_with_valid_role(self):
        user, headers = self.get_user_and_headers()
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            response = self.admin_view()
            self.assertEqual({"error": "Unauthorized User!!"}, response[0].json)
            self.assertEqual(401, response[1])

    def test_allowed_roles_decorator_with_unauthorized_user(self):
        user, headers = self.get_user_and_headers()
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            response = self.user_view()
            self.assertEqual(response, "success")

    def test_allowed_roles_decorator_with_invalid_access_token(self):
        invalid_access_token = create_access_token(identity={"user_id": 999})
        headers = {"Authorization": f"Bearer {invalid_access_token}"}
        with self.app.test_request_context(headers=headers):
            verify_jwt_in_request()
            response = self.user_view()
            self.assertEqual({"error": "User Not Found !!"}, response[0].json)
            self.assertEqual(403, response[1])
