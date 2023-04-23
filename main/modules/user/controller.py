from main.modules.jwt.controller import JWTController
from main.modules.user.model import User


class UserController:
    """
    UserController is used to handle all operations related to user.
    """

    @classmethod
    def get_current_user_profile(cls) -> User:
        """
        This function is used to get the profile of logged-in user.
        :return:
        """
        identity = JWTController.get_user_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        return user.serialize()

    @classmethod
    def update_user_profile(cls, user_data: dict):
        """
        This function is used to update the profile.
        :param user_data:
        :return:
        """
        identity = JWTController.get_user_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        user.update(user_data)

    @classmethod
    def get_profiles(cls):
        """
        This function is used to get all user profiles.
        :return:
        """
        users = User.query.all()
        return [user.serialize() for user in users]
