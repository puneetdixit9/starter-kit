# from unittest import TestCase, mock

# from src.decorators.user_role import allowed_roles


# class TestAllowedRolesDecorator(TestCase):

#     def setUp(self):
#         self.mock_request = mock.MagicMock()
#         self.mock_request.headers = {"Authorization": "Bearer token"}

#     @allowed_roles(["admin"])
#     def mock_view(self):
#         return "success"

#     def test_allowed_roles_decorator_with_valid_role(self):
#         with mock.patch("src.decorators.auth.User.query") as mock_query:
#             mock_user = mock.MagicMock()
#             mock_user.role = "admin"
#             mock_query.filter_by().first.return_value = mock_user
#             response = self.mock_view(self.mock_request)
#             self.assertEqual(response, "success")

#     def test_allowed_roles_decorator_with_invalid_role(self):
#         with mock.patch("src.decorators.auth.User.query") as mock_query:
#             mock_user = mock.MagicMock()
#             mock_user.role = "user"
#             mock_query.filter_by().first.return_value = mock_user
#             response = self.mock_view(self.mock_request)
#             self.assertEqual(response.status_code, 401)

#     def test_allowed_roles_decorator_with_nonexistent_user(self):
#         with mock.patch("src.decorators.auth.User.query") as mock_query:
#             mock_query.filter_by().first.return_value = None
#             response = self.mock_view(self.mock_request)
#             self.assertEqual(response.status_code, 403)
