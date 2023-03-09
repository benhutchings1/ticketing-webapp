from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import current_config
from models import User, TokenBlocklist
from exts import db
# from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, \
    unset_jwt_cookies, get_jwt, get_jwt_identity, current_user
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config.from_object(current_config)
db.init_app(app)
# migrate=Migrate(app,db)

# initializing a JWTManager with this app
jwt = JWTManager(app)
api = Api(app, doc='/docs')

# signup expected input
signup_model = api.model(
    "SignUp",
    {
        "email_address": fields.String(max_length=100),  # max_length=100
        "password": fields.String(max_length=16),
        "firstname": fields.String(max_length=20),
        "surname": fields.String(max_length=20),
        "date_of_birth": fields.Date(),
        "postcode": fields.String(max_length=7),
        "phone_number": fields.String(max_length=14),
        "role": fields.String(max_length=100)
    }
)

# Login expected input
login_model = api.model(
    "LogIn",
    {
        "email_address": fields.String(max_length=100),
        "password": fields.String(max_length=16)
    }
)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_blocked(jwt_header, jwt_payload: dict) -> bool:
    # Checks if token is in blocked list
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@app.after_request
def refresh_expiring_jwts(response):
    try:
        if response.json.get('logout', False):
            # Do nothing if logging out
            return response

        # Update JWT close to expiring
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Invalid JWT, return unchanged response
        return response


@api.route('/signup')
class SignUp(Resource):

    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        email_address = data.get('email_address')

        # user already exists in database?
        db_email_address = User.query.filter_by(email_address=email_address).first()
        if db_email_address is not None:
            return jsonify({"success": False, "message": f"The user {email_address} already exits."})

        # add new user
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
        return jsonify({"success": True, "message": f"User {email_address} created successfully."})


@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        data = request.get_json()

        email_address = data.get('email_address')
        password = data.get('password')

        db_user = User.query.filter_by(email_address=email_address).first()

        if db_user and check_password_hash(db_user.passwd_hash, password):
            # Login was successful
            response = jsonify({"success": True, "message": "Successfully logged in"})
            access_token = create_access_token(identity=db_user.user_id)
            set_access_cookies(response, access_token)
            return response

        # Login failure
        return jsonify({"success": False, "message": "Incorrect email/password"})


@api.route('/logout')
class Logout(Resource):

    @jwt_required()
    def post(self):
        # Unset cookies
        response = jsonify({"success": True, "message": "Successfully logged out", "logout": True})
        unset_jwt_cookies(response)

        # Revoke cookie
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now(timezone.utc)))
        db.session.commit()

        return response


@api.route('/account')
class Account(Resource):

    @jwt_required()
    def get(self):
        return jsonify({"email": current_user.email_address,
                        "firstname": current_user.firstname,
                        "surname": current_user.surname,
                        "date_of_birth": current_user.date_of_birth,
                        "postcode": current_user.postcode,
                        "phone_number": current_user.phone_number})


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "UserTable": User
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
