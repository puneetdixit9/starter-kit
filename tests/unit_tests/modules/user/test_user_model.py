import pytest

from main.modules.auth.model import AuthUser
from main.modules.user.model import User


class TestAuthModel:
    @pytest.fixture(scope="class", autouse=True)
    def add_fixtures(self, load_data_from_file):
        load_data_from_file(AuthUser, "unit_tests/fixtures/auth_users.json")

    def test_get_user_profiles(self, app):
        with app.app_context():
            users = User.query.all()
            assert len(users) == 2
