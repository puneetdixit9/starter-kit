from main.modules.jwt.controller import JWTController
from main.modules.user.model import User


class UserController:
    """
    UserController is used to handle all operations related to user.
    """

    @classmethod
    def get_profile(cls, user_id: int = None) -> dict:
        """
        To get the profile of user.
        :return:
        """
        if not user_id:
            user_id = JWTController.get_user_identity()["user_id"]
        user = User.query.filter_by(id=user_id).first()
        return user.serialize()

    @classmethod
    def update_user_profile(cls, user_data: dict, user_id: int = None):
        """
        To update the profile.
        :param user_id:
        :param user_data:
        :return:
        """
        if not user_id:
            user_id = JWTController.get_user_identity()["user_id"]
        user = User.query.filter_by(id=user_id).first()
        user.update(user_data)

    @classmethod
    def get_profiles(cls) -> list[dict]:
        """
        To get all user profiles.
        :return:
        """
        users = User.query.all()
        return [user.serialize() for user in users]
