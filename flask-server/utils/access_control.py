from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user


def management_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        if current_user.role == "management":
            return fn(*args, **kwargs)
        else:
            return jsonify({'msg': "Role 'management' is required"})

    return decorator
