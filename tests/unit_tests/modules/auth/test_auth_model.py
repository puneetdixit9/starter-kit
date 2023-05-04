import pytest

from main.modules.auth.model import AuthUser

TEST_USER_ID = 1


class TestAuthModel:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file):
        load_data_from_file(AuthUser, "unit_tests/fixtures/auth_users.json")

    def test_get_all_users(self, app):
        with app.app_context():
            auth_users = AuthUser.query.all()
            assert len(auth_users) == 2

    def test_create_user(self, app):
        with app.app_context():
            user_data = {
                "username": "Puneet",
                "role": "admin",
                "email": "puneet@gmail.com",
                "password": "1234",
            }
            auth_user = AuthUser.create(user_data)
            assert auth_user.username == "Puneet"
            assert auth_user.role == "admin"
            assert auth_user.email == "puneet@gmail.com"
            assert auth_user.password == "1234"

    def test_update_user(self, app):
        with app.app_context():
            auth_user = AuthUser.query.filter_by(id=TEST_USER_ID).first()
            assert auth_user.updated_at is None
            assert auth_user.password != "updatedtestpassword"

            auth_user.update({"password": "updatedtestpassword"})

            assert auth_user.updated_at is not None
            assert auth_user.password == "updatedtestpassword"

    def test_delete_user(self, app):
        with app.app_context():
            auth_user = AuthUser.query.filter_by(id=TEST_USER_ID).first()
            assert auth_user is not None
            AuthUser.delete(id=TEST_USER_ID)

            auth_user = AuthUser.query.filter_by(id=TEST_USER_ID).first()
            assert auth_user is None
