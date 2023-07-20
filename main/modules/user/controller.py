from main.modules.jwt.controller import JWTController
from main.modules.auth.model import AuthUser
from main.modules.log_event.controller import LogEventController


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
        user = AuthUser.query.filter_by(id=user_id).first()
        user = user.serialize()
        LogEventController.log_event("get_user_profile", user_id, user['tid'] , "NONE")
        return user

    @classmethod
    def update_user_profile(cls, user_data: dict, user_id: int):
        """
        To update the profile.
        :param user_id:
        :param user_data:
        :return:
        """
        # if not user_id:
        #     user_id = JWTController.get_user_identity()["user_id"]
        user = AuthUser.query.filter_by(id=user_id).first()
        user_dict = vars(user)
        print(user_dict)
        LogEventController.log_event("update_user_profile", user_id, user_dict['tid'])
        user.update(user_data)

    @classmethod
    def get_profiles(cls) -> list[dict]:
        """
        To get all user profiles.
        :return:
        """
        LogEventController.log_event("get_profiles", "ADMIN", "ADMIN" , "users/profileList")
        users = AuthUser.query.all()
        return [user.serialize() for user in users]
