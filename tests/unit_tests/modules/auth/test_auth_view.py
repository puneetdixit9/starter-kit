from unittest.mock import MagicMock

from flask import Response
from flask_jwt_extended import create_access_token

from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from main.modules.auth.view import ChangePassword, Login, Logout, Refresh, SignUp
from tests.utils import (
    get_update_password_data,
    get_user_role_login_credentials,
    get_user_role_signup_data,
)

USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2


def get_user_and_headers(app, user_id: int = USER_ROLE_ID):
    with app.app_context():
        auth_user = AuthUser.query.filter_by(id=user_id).first()
        access_token = create_access_token(identity={"user_id": user_id})
        headers = {"Authorization": f"Bearer {access_token}"}
        return auth_user, headers


class TestSignUpApi:
    def setup_method(self):
        self.api = SignUp()

    def test_post(self, app, mocker):
        mock_user = MagicMock()
        mock_user.id = 123

        mocker.patch.object(AuthUserController, "create_new_user", return_value=(mock_user, {}))

        signup_data = get_user_role_signup_data()
        with app.test_request_context("/auth/signup", json=signup_data):
            response = self.api.post()

        assert isinstance(response, Response)
        assert response.status_code == 201
        assert response.json["id"] == 123

        mocker.patch.object(
            AuthUserController, "create_new_user", return_value=(None, {"error": "user already exists"})
        )

        with app.test_request_context("/auth/signup", json=signup_data):
            response = self.api.post()

        assert isinstance(response, Response)
        assert response.status_code == 409
        assert response.json["error"] == "user already exists"


class TestLoginApi:
    def setup_method(self):
        self.api = Login()

    def test_post(self, app, mocker):
        mocker.patch.object(AuthUserController, "get_token", return_value=({}, {}))

        login_data = get_user_role_login_credentials()
        with app.test_request_context("/auth/login", json=login_data):
            response = self.api.post()

        assert isinstance(response, Response)
        assert response.status_code == 200

        mocker.patch.object(AuthUserController, "get_token", return_value=(None, {"error": "Invalid password"}))

        with app.test_request_context("/auth/login", json=login_data):
            response = self.api.post()

        assert isinstance(response, Response)
        assert response.status_code == 403


class TestRefresh:
    def setup_method(self):
        self.api = Refresh()

    def test_get(self, app, mocker):
        mocker.patch.object(AuthUserController, "refresh_access_token", return_value={})

        with app.test_request_context("/auth/refresh"):
            response = self.api.get()

        assert isinstance(response, Response)
        assert response.status_code == 200


class TestChangePassword:
    def setup_method(self):
        self.api = ChangePassword()

    def test_put(self, app, mocker):
        mocker.patch.object(AuthUserController, "update_user_password", return_value=({}, {}))

        with app.test_request_context("/auth/change_password", json=get_update_password_data()):
            response = self.api.put()

        assert isinstance(response, Response)
        assert response.status_code == 200

        mocker.patch.object(
            AuthUserController, "update_user_password", return_value=({}, {"error": "old password is wrong"})
        )
        with app.test_request_context("/auth/change_password", json=get_update_password_data()):
            response = self.api.put()

        assert isinstance(response, Response)
        assert response.status_code == 401


class TestLogout:
    def setup_method(self):
        self.api = Logout()

    def test_delete(self, app, mocker):
        mocker.patch.object(AuthUserController, "logout", return_value={})

        with app.test_request_context("/auth/logout"):
            response = self.api.delete()

        assert isinstance(response, Response)
        assert response.status_code == 200
