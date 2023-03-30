from flask import Blueprint
from project.models.user_models import Address
from project.schema_validators.auth_schema_validators import ROLE
from flask import request, jsonify
from project.utils.utils import (
    get_user,
    allowed_roles,
    create_address_response,
    update_address_with_new_values
)
from project import db
from marshmallow import ValidationError
from datetime import datetime
from flask_jwt_extended import jwt_required

from project.schema_validators.main_schema_validators import (
    AddAddressSchema,
    UpdateAddressSchema
)

main_router = Blueprint('main', __name__)


@main_router.route('/', methods=['GET'])
def server_status():
    return jsonify({"message": "server is up"}), 200


@main_router.route('/address', methods=["POST"])
@jwt_required()
@allowed_roles([ROLE.USER.value])  # Allowed to role type User only.
def add_address():
    data = request.json
    schema = AddAddressSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data.update({
        "user_id": get_user().id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    address = Address(**data)
    db.session.add(address)
    db.session.commit()

    return jsonify({'address_id': address.id, "status": "success"}), 201


@main_router.route('/addresses', methods=["GET"])
@jwt_required()
@allowed_roles([ROLE.ADMIN.value, ROLE.USER.value])  # Allowed for Admin and User role type.
def get_addresses():
    user = get_user()
    if user.role == ROLE.USER.value:
        data = Address.query.filter_by(user_id=user.id)
    else:
        user_id = request.args.get("id")
        if user_id:
            data = Address.query.filter_by(user_id=user_id)
        else:
            data = Address.query.all()
    return jsonify(create_address_response(data)), 200


@main_router.route('/address', methods=['PUT'])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def update_address():
    data = request.json
    schema = UpdateAddressSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    address = Address.query.filter_by(id=data["address_id"]).first()
    if not address:
        return jsonify({
            'message': 'address_id not found'}
        ), 403
    if address.user_id != get_user().id:
        return jsonify({
            'message': 'Unauthorized User!!'
        }), 401
    update_address_with_new_values(address, data)
    db.session.commit()
    return jsonify({'message': 'Success'}), 200


@main_router.route('/address/<address_id>', methods=['DELETE'])
@jwt_required()
@allowed_roles([ROLE.USER.value])
def delete_address(address_id):
    address = Address.query.filter_by(id=address_id).first()
    if not address:
        return jsonify({
            'message': 'Wrong address_id'
        }), 404
    elif address.user_id != get_user().id:
        return jsonify({
            'message': 'Unauthorized User!!'
        }), 401

    Address.query.filter_by(id=address_id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Success'
    }), 200
