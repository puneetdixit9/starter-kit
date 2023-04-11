import settings
from flask import jsonify

from src.database.models.auth import User, TokenBlocklist
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from src.database import db
from src.utils import update_class_object
from werkzeug.security import generate_password_hash, check_password_hash
import enum


class ROLE(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class AuthManager:
    @classmethod
    def get_current_user(cls):
        identity = get_jwt_identity()
        return User.query.filter_by(id=identity["user_id"]).first()

    @classmethod
    def get_current_user_profile(cls):
        identity = get_jwt_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        return user.as_dict()

    @classmethod
    def create_new_user(cls, user_data):
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
    def update_user_profile(cls, user_data):
        identity = get_jwt_identity()
        user = User.query.filter_by(id=identity["user_id"]).first()
        update_class_object(user, user_data)
        db.session.commit()

    @classmethod
    def update_user_password(cls, update_password_data={}):
        user = cls.get_current_user()
        if check_password_hash(user.password, update_password_data['old_password']):
            if check_password_hash(user.password, update_password_data['new_password']):
                return jsonify(error="new password can not same as old password"), 403
            user.password = generate_password_hash(update_password_data['new_password'])
            db.session.commit()
            return jsonify({"status": "success"}), 200
        return jsonify(error='Old password is invalid'), 403

    @classmethod
    def get_token(cls, login_data):
        email_or_username = login_data.get("username") or login_data.get("email")
        user = db.session.query(User).filter(
            (User.email == email_or_username) | (User.username == email_or_username)).first()
        if not user:
            return {"error": f"user not found with {email_or_username}"}, 403

        if check_password_hash(user.password, login_data['password']):
            access_token = create_access_token(identity={"user_id": user.id})
            refresh_token = create_refresh_token(identity={"user_id": user.id})
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expire_in": settings.TOKEN_EXPIRE_IN * 60
            }, 200
        return {"error": "wrong password"}, 403
    
    @classmethod
    def logout(cls):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        user = cls.get_current_user()
        db.session.add(TokenBlocklist(jti=jti, type=ttype, user_id=user.id))
        db.session.commit()
        return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")

    @classmethod
    def token_revoked_check(cls, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @classmethod
    def refresh_access_token(cls):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token, expire_in=60 * settings.TOKEN_EXPIRE_IN)