from flask import jsonify
from flask_bcrypt import check_password_hash

from db import db
from models.auth_tokens import AuthTokens, auth_token_schema
from models.users import Users
from datetime import datetime, timedelta


def auth_token_add(req):
    post_data = req.form if req.form else req.json

    fields = ['email', 'password']
    req_fields = ['email', 'password']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        values[field] = field_data
        if field in req_fields and not values[field]:
            return jsonify(f'{field} is required'), 400

    user_data = db.session.query(Users).filter(Users.email == values['email']).first()

    if not user_data:
        return jsonify({"message": "invalid login"}), 401

    valid_password = check_password_hash(user_data.password, values['password'])

    if not valid_password:
        return jsonify({"message": "invalid login"}), 401

    if not user_data.active:
        return jsonify({"message": "account has been deactivated"}), 403

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()

    expiry = datetime.now() + timedelta(hours=12)

    if existing_tokens:
        for token in existing_tokens:
            if token.expiration < datetime.now():
                db.session.delete(token)

    new_token = AuthTokens(user_data.user_id, expiry)

    db.session.add(new_token)
    db.session.commit()

    return jsonify({"auth_info": auth_token_schema.dump(new_token)}), 201
