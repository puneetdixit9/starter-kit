import settings
from project import db, jwt
from project.schema_validators.auth_schema_validators import SignUpSchema, LogInSchema, UpdatePassword
from flask import Blueprint
from project.models.user_models import User
from project.models.token_model import TokenBlocklist

from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from project.utils.utils import get_user
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)

auth_router = Blueprint('auth', __name__)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@auth_router.route('/login', methods=['POST'])
def login():
    data = request.json
    schema = LogInSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        # returns 403 if user does not exist
        return make_response('User does not exist with provided email', 403,
                             {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
    if check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity={"user_id": user.id})
        refresh_token = create_refresh_token(identity={"user_id": user.id})
        return jsonify(access_token=access_token, refresh_token=refresh_token, expire_in=60 * settings.TOKEN_EXPIRE_IN,
                       role=user.role)

    # returns 403 if password is wrong
    return make_response('Wrong Password', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'})


@auth_router.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token, expire_in=60 * settings.TOKEN_EXPIRE_IN)


@auth_router.route('/signup', methods=["POST"])
def signup():
    data = request.json
    schema = SignUpSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # checking for existing user
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        data["password"] = generate_password_hash(data["password"])
        user = User(**data)
        # insert user
        db.session.add(user)
        db.session.commit()

        return jsonify({'user_id': user.id, "status": "success"}), 201

    # returns 202 if user already exists
    return make_response('User already exists. Please Log in.', 409)


@auth_router.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.json
    schema = UpdatePassword()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = get_user()
    if check_password_hash(user.password, data['old_password']):
        if check_password_hash(user.password, data['new_password']):
            return make_response('new password can not same as old password', 403)
        user.password = generate_password_hash(data['new_password'])
        db.session.commit()
        return jsonify({"status": "success"}), 200
    return make_response('Old password is invalid', 403)


@auth_router.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    db.session.add(TokenBlocklist(jti=jti, type=ttype))
    db.session.commit()
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")
