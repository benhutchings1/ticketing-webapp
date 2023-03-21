from datetime import datetime, timedelta

from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, get_jti

from exts import db
from models import Token


def login_user_response(user, data=None):
    """Adds user login with cookie to response"""
    if data is None:
        data = {}

    # Revoke all previous token
    Token.query.filter(Token.user_id == user.user_id).delete()

    # Create token for user
    access_token = create_access_token(identity=user.user_id)
    user.jti = get_jti(access_token)
    user.last_update = datetime.now()

    # Add token
    token = Token(jti=user.jti, exp_date=datetime.now() + timedelta(hours=1), user_id=user.user_id)
    db.session.add(token)

    # Save changes
    db.session.commit()

    # Set for session
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
