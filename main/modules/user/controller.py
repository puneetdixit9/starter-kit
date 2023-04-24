from main.modules.jwt.controller import JWTController
from main.modules.user.model import User


class UserController:
    """
    UserController is used to handle all operations related to user.
    """

    @classmethod
    def get_profile(cls, user_id: int = None) -> dict:
        """
        This function is used to get the profile of user by user_id, If user_id is not provided then it
        will use current logged-in user id.
        :return:
        """
        if not user_id:
            user_id = JWTController.get_user_identity()["user_id"]
        user = User.query.filter_by(id=user_id).first()
        return user.serialize()

    @classmethod
    def update_user_profile(cls, user_data: dict, user_id: int = None):
        """
        This function is used to update the profile.
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
        This function is used to get all user profiles.
        :return:
        """
        users = User.query.all()
        return [user.serialize() for user in users]
