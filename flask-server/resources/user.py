import re
from datetime import datetime, timezone

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user, get_jwt, unset_jwt_cookies
from flask_restx import Resource, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
from models import User, Token
from utils.response import login_user_response

ns = Namespace('/user')

# /signup expected input
signup_model = ns.model(
    "SignUp",
    {
        "email_address": fields.String(max_length=100),
        "password": fields.String(max_length=16),
        "firstname": fields.String(max_length=20),
        "surname": fields.String(max_length=20),
        "date_of_birth": fields.Date(),
        "postcode": fields.String(max_length=7),
        "phone_number": fields.String(max_length=14)
    }
)

# /login expected input
login_model = ns.model(
    "LogIn",
    {
        "email_address": fields.String(max_length=100),
        "password": fields.String(max_length=16)
    }
)


def check_signup(data) -> (bool, str):
    """Returns if signup is valid with error message if invalid"""
    # Check if user already exists
    email_address = data.get('email_address')
    db_user = User.query.filter_by(email_address=email_address).first()
    if db_user is not None:
        return False, f"{email_address} already has an account"

    # Email check
    email_format = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if not re.match(email_format, email_address):
        return False, f"{email_address}: invalid email address format"

    # Password check
    password = data.get('password')
    if len(password) < 8:
        return False, f"Password length must be 8 or less"

    # Phone number uniqueness check + format check
    phone_number = data.get('phone_number')
    db_user = User.query.filter_by(phone_number=phone_number).first()
    if db_user is not None:
        return False, f"Another user has this {db_user.phone_number} phone number"
    if len(phone_number) > 16:
        return False, f"Phone number must be 16 digits or less"
    if not phone_number.isnumeric():
        return False, f"Phone number must be numeric"

    # Format checks for firstname & surname
    firstname = data.get('firstname')
    surname = data.get('surname')
    if len(firstname) > 32 or len(surname) > 32:
        return False, f"The firstname & surname must be 32 characters or less"

    # Format check for postcode
    dob = data.get('date_of_birth')
    try:
        datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        return False, f"Date of birth must be valid"

    # Format check for postcode
    postcode = data.get('postcode')
    if len(postcode) > 8:
        return False, f"Postcode length must be 8 or more"

    # All checks passed
    return True, ""


# Signup route with format & uniquemess checks (to avoid unuseful internal server errors)
@ns.route('/signup')
class SignUp(Resource):
    @ns.expect(signup_model)
    def post(self):
        data = request.get_json()

        # Check if signup is valid
        success, msg = check_signup(data)
        if not success:
            response = jsonify({"msg": msg})
            response.status_code = 400
            return response

        # Add new user
        new_user = User(
            email_address=data.get('email_address'),
            # salted hash
            passwd_hash=generate_password_hash(data.get('password'), method="sha256", salt_length=32),
            firstname=data.get('firstname'),
            surname=data.get('surname'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), "%Y-%m-%d").date(),
            postcode=data.get('postcode'),
            phone_number=data.get('phone_number'),
            role='user'
        )
        new_user.save()

        response_data = {"msg": f"User {data.get('email_address')} created successfully."}
        return login_user_response(new_user, response_data)


@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.get_json()

        email_address = data.get('email_address')
        password = data.get('password')

        db_user = User.query.filter_by(email_address=email_address).first()

        if db_user and check_password_hash(db_user.passwd_hash, password):
            # Login was successful
            return login_user_response(db_user, data={"msg": "Successfully logged in"})

        # Login failure
        response = jsonify({'msg': 'Incorrect email/password'})
        response.status_code = 401
        return response


@ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        # Revoke cookie
        current_user.jti = None
        current_user.update()

        # Revoke token
        Token.query.filter(Token.user_id == current_user.user_id).delete()
        db.session.commit()

        # Unset cookies
        response = jsonify({"success": True, "message": "Successfully logged out", "logout": True})
        unset_jwt_cookies(response)

        return response


@ns.route('/account')
class Account(Resource):
    @jwt_required()
    def get(self):
        return jsonify({"user_id": current_user.user_id,
                        "email": current_user.email_address,
                        "firstname": current_user.firstname,
                        "surname": current_user.surname,
                        "date_of_birth": str(current_user.date_of_birth),
                        "postcode": current_user.postcode,
                        "phone_number": current_user.phone_number,
                        "role": current_user.role})
