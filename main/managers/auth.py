import enum

from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash

import settings
from src.database import db
from src.database.models.auth import TokenBlocklist, User
from src.utils import update_class_object


class ROLE(enum.Enum):
    """
    ROLE is an enum of valid roles in the system.
    """

    ADMIN = "admin"
    USER = "user"


class AuthManager:
    """
    AuthManger is used to handle all operations related and user and authentication.
    """

    @classmethod
    def get_current_user(cls) -> User:
        """
        This function is used to get the User object of current logged-in user based on jwt
        token in request headers.
        :return User:
        """
        identity = get_jwt_identity()
        return User.query.filter_by(id=identity["user_id"]).first()

    @classmethod
    def get_current_user_profile(cls) -> dict:
        """
        This function is used to get the profile of logged-in user. It returns response in dict
        form.
        :return dict:
        """
        identity = get_jwt_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        return user.as_dict()

    @classmethod
    def create_new_user(cls, user_data: dict) -> (User, dict):
        """
        This function is used to create new user in the databases. Also, it is used to check if
        username or email already exists or not.
        :param user_data:
        :return (User, error_data):
        """
        error_data = {}
        user_by_email = User.query.filter_by(email=user_data["email"]).first()
        user_by_username = User.query.filter_by(username=user_data["username"]).first()
        if user_by_email or user_by_username:
            param = "username" if user_by_username else "email"
            error_data["error"] = f"user already exists with provided {param}"
        else:
            user_data["password"] = generate_password_hash(user_data["password"])
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            return user, error_data
        return None, error_data

    @classmethod
    def update_user_profile(cls, user_data: dict):
        """
        This function is used to update the profile.
        :param user_data:
        :return:
        """
        identity = get_jwt_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        update_class_object(user, user_data)
        db.session.commit()

    @classmethod
    def update_user_password(cls, update_password_data: dict) -> (dict, str):
        """
        This function is used to change the password.
        :param update_password_data:
        :return dict, error_msg:
        """
        user = cls.get_current_user()
        if check_password_hash(user.password, update_password_data["old_password"]):
            if check_password_hash(user.password, update_password_data["new_password"]):
                return {}, "new password can not same as old password"
            user.password = generate_password_hash(update_password_data["new_password"])
            db.session.commit()
            return {"status": "success"}, ""
        return {}, "Old password is invalid"

    @classmethod
    def get_token(cls, login_data: dict) -> (dict, str):
        """
        This function is used to get the token using email or username and password. It returns
        access_token and refresh_token.
        :param login_data:
        :return dict:
        """
        token = {}
        error = ""
        email_or_username = login_data.get("username") or login_data.get("email")
        user = (
            db.session.query(User)
            .filter((User.email == email_or_username) | (User.username == email_or_username))
            .first()
        )
        if not user:
            return token, f"user not found with {email_or_username}"

        if check_password_hash(user.password, login_data["password"]):
            access_token = create_access_token(identity={"user_id": user.id})
            refresh_token = create_refresh_token(identity={"user_id": user.id})
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expire_in": settings.TOKEN_EXPIRE_IN * 60,
            }, error
        return token, "wrong password"

    @classmethod
    def logout(cls):
        """
        This function is used to revoke the access and refresh token when user logged-out and add
        that token in blocklist so that no one can use that token.
        :return:
        """
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        user = cls.get_current_user()
        db.session.add(TokenBlocklist(jti=jti, type=ttype, user_id=user.id))
        db.session.commit()
        return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")

    @classmethod
    def token_revoked_check(cls, jwt_payload: dict) -> TokenBlocklist or None:
        """
        This function is used to check the jwt token  is revoked or not (If it is present in
        the TokenBlocklist then it is revoked.)
        :param jwt_payload:
        :return:
        """
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @classmethod
    def refresh_access_token(cls) -> dict:
        """
        This function is used to get a new access token.
        :return:
        """
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token, "expire_in": 60 * settings.TOKEN_EXPIRE_IN}
