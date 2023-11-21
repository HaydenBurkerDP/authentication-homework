import functools
from flask import Response
from datetime import datetime

from db import db
from models.auth_tokens import AuthTokens
from util.validate_uuid4 import validate_uuid4


def validate_auth_token(arg_zero):
    auth_token = arg_zero.headers["auth"]

    if not auth_token or not validate_uuid4(auth_token):
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token and existing_token.expiration > datetime.now():
        return existing_token

    else:
        return False


def failure_response():
    return Response("authentication required", 401)


def authenticate(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_token = validate_auth_token(args[0])

        if auth_token:
            return func(*args, **kwargs)
        else:
            return failure_response()

    return wrapper_authenticate


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_token = validate_auth_token(args[0])
        kwargs["auth_info"] = auth_token

        if auth_token:
            return func(*args, **kwargs)
        else:
            return failure_response()

    return wrapper_authenticate
