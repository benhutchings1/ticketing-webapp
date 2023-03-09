from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import User
from exts import db
# from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, set_access_cookies, \
    unset_jwt_cookies, set_refresh_cookies
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
# migrate=Migrate(app,db)

# initializing a JWTManager with this app
JWTManager(app)
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


@api.route('/signup')
class SignUp(Resource):

    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        email_address = data.get('email_address')

        # user already exists in database?
        db_email_address = User.query.filter_by(email_address=email_address).first()
        if db_email_address is not None:
            return jsonify({"message": f"The user {email_address} already exits."})

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
            role=data.get('phone_number')
        )
        new_user.save()
        return jsonify({"message": f"User {email_address} created successfully."})


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
            response = jsonify({"status": "success", "message": "Successfully logged in"})
            access_token = create_access_token(identity=db_user.user_id)
            refresh_token = create_refresh_token(identity=db_user.user_id)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        # Login failure
        return jsonify({"status": "failure", "message": "Incorrect email/password"})


@api.route('/logout')
class Logout(Resource):

    def post(self):
        response = jsonify({"status": "success", "message": "Successfully logged out"})
        unset_jwt_cookies(response)
        return response


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
