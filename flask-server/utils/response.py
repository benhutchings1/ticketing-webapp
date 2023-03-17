from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies


def login_user_response(user, data=None):
    """Adds user login with cookie to response"""
    if data is None:
        data = {}
    access_token = create_access_token(identity=user.user_id)
    data['token'] = access_token
    response = jsonify(data)
    set_access_cookies(response, access_token)
    return response


def msg_response(msg, data=None, status_code=200):
    """Creates a response that includes msg and other data passed with the given status code"""
    if not data:
        data = {}
    response_data = data
    response_data.update({"msg": msg})
    response = jsonify(response_data)
    response.status_code = status_code
    return response
