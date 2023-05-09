from flask import Response
from flask_jwt_extended import create_access_token, verify_jwt_in_request

from main.modules.auth.model import AuthUser
from main.modules.user.controller import UserController
from main.modules.user.view import Profile, Profiles, Profiles2

USER_ROLE_ID = 1
ADMIN_ROLE_ID = 2


def get_user_and_headers(app, user_id: int = USER_ROLE_ID):
    with app.app_context():
        auth_user = AuthUser.query.filter_by(id=user_id).first()
        access_token = create_access_token(identity={"user_id": user_id})
        headers = {"Authorization": f"Bearer {access_token}"}
        return auth_user, headers


class TestProfile:
    def setup_method(self):
        self.api = Profile()

    def test_get(self, app, mocker):
        mocker.patch.object(UserController, "get_profile", return_value={})
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/user/profile", headers=headers):
            verify_jwt_in_request()
            response = self.api.get()

        assert isinstance(response, Response)
        assert response.status_code == 200

    def test_put(self, app, mocker):
        _, headers = get_user_and_headers(app)
        mocker.patch.object(UserController, "update_user_profile", return_value={})
        with app.test_request_context("/user/profile", headers=headers, json={"department": "test"}):
            verify_jwt_in_request()
            response = self.api.put()

        assert isinstance(response, Response)
        assert response.status_code == 200


class TestProfiles:
    def setup_method(self):
        self.api = Profiles()

    def test_get(self, app, mocker):
        mocker.patch.object(UserController, "get_profiles", return_value=[])
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/user/profiles", headers=headers):
            verify_jwt_in_request()
            response = self.api.get()

        assert isinstance(response, Response)
        assert response.status_code == 200


class TestProfiles2:
    def setup_method(self):
        self.api = Profiles2()

    def test_get(self, app, mocker):
        mocker.patch.object(UserController, "get_profile", return_value={})
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/user/profiles/1", headers=headers):
            verify_jwt_in_request()
            response = self.api.get(1)

        assert isinstance(response, Response)
        assert response.status_code == 200

    def test_put(self, app, mocker):
        mocker.patch.object(UserController, "update_user_profile", return_value={})
        _, headers = get_user_and_headers(app)
        with app.test_request_context("/user/profiles/1", headers=headers, json={"department": "test"}):
            verify_jwt_in_request()
            response = self.api.put(1)

        assert isinstance(response, Response)
        assert response.status_code == 200
