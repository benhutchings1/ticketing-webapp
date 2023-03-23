from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from utils.response import msg_response


def management_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        if current_user.role == "management":
            return fn(*args, **kwargs)
        else:
            return msg_response("Role 'management' is required", status_code=401)

    return decorator
