from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from config import current_config
from models import *
from exts import db
# from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, \
    unset_jwt_cookies, get_jwt, get_jwt_identity, current_user, verify_jwt_in_request
from datetime import datetime, timedelta, timezone
import utils
from sqlalchemy.exc import IntegrityError
import re

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://localhost:3000"])
app.config.from_object(current_config)
db.init_app(app)
# migrate=Migrate(app,db)

# initializing a JWTManager with this app
jwt = JWTManager(app)
api = Api(app, doc='/docs')

# /signup expected input
signup_model = api.model(
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
login_model = api.model(
    "LogIn",
    {
        "email_address": fields.String(max_length=100),
        "password": fields.String(max_length=16)
    }
)

# /add_event expected input
event_model = api.model(
    "Event",
    {
        "event_name": fields.String(max_length=128),
        "datetime": fields.String(),  # e.g. '2023-03-09 12:10:00'
        "genre": fields.String(max_length=128),
        "description": fields.String(),
        "venue_name": fields.String(max_length=128),
        "venue_location": fields.String(max_length=200),
        "venue_postcode": fields.String(max_length=8),
        "venue_capacity": fields.Integer()
    }
)

# Search by event name model
search_event_model = api.model(
    "SearchEvent",
    {
        "event_name": fields.String(),
    }
)

# /addticket expected input model
add_ticket_input_model = api.model(
    "AddTicket",
    {
        "event_id": fields.Integer(required=True, min=0),
        "ticket_type": fields.String(required=True),
        "token": fields.String(required=True, max_length=128)
    }
)

# Request QR code data input model
request_qr_data_model = api.model(
    "RequestQRdata",
    {
        "ticket_id": fields.Integer(min=0, required=True)
    }
)

# Validate Ticket input model
validate_ticket_model = api.model(
    "ValidateTicket",
    {
        "event_id": fields.Integer(min=0, required=True),
        "ticket_id": fields.Integer(min=0, required=True),
        "qr_data": fields.String(required=True)
    }
)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()


def management_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        if current_user.role == "management":
            return fn(*args, **kwargs)
        else:
            return jsonify({'msg': "Role 'management' is required"})

    return decorator


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
    except (RuntimeError, KeyError, AttributeError):
        # Invalid JWT, return unchanged response
        return response


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


def check_signup(data) -> (bool, str):
    """Returns if signup is valid with error message if invalid"""
    # Check if user already exists
    email_address = data.get('email_address')
    db_user = User.query.filter_by(email_address=email_address).first()
    if db_user is not None:
        return False, f"The user {email_address} already exits."

    # Email check
    email_format = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if not re.match(email_format, email_address):
        return False, f"{email_address}: invalid email address format."

    # Phone number uniqueness check + format check
    phone_number = data.get('phone_number')
    db_user = User.query.filter_by(phone_number=phone_number).first()
    if db_user is not None:
        return False, f"Another user has this {db_user.phone_number} phone number."
    if len(phone_number) > 16:
        return False, f"Phone number must be 16 digits or less."
    if not phone_number.isnumeric():
        return False, f"Phone number must be numeric."

    # Format checks for firstname & surname
    firstname = data.get('firstname')
    surname = data.get('surname')
    if len(firstname) > 32 or len(surname) > 32:
        return False, f"The firstname & surname must be 32 characters or less."

    # Format check for postcode
    postcode = data.get('postcode')
    if len(postcode) > 8:
        return False, f"Postcode length must be 8 or less."

    # All checks passed
    return True, ""


# Signup route with format & uniquemess checks (to avoid unuseful internal server errors)
@api.route('/signup')
class SignUp(Resource):
    @api.expect(signup_model)
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
            return login_user_response(db_user, data={"msg": "Successfully logged in"})

        # Login failure
        response = jsonify({'msg': 'Incorrect email/password'})
        response.status_code = 401
        return response


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
        return jsonify({"user_id": current_user.user_id,
                        "email": current_user.email_address,
                        "firstname": current_user.firstname,
                        "surname": current_user.surname,
                        "date_of_birth": str(current_user.date_of_birth),
                        "postcode": current_user.postcode,
                        "phone_number": current_user.phone_number,
                        "role": current_user.role})


''' 
This route adds a new event
To do so, it also adds a new venue if not already in DB
'''


@api.route('/add_event')
class AddEvent(Resource):
    @api.expect(event_model)
    @management_required
    def post(self):

        data = request.get_json()
        event_name = data.get('event_name')
        venue_name = data.get('venue_name')

        # event already exists in database?
        db_event_name = Event.query.filter_by(event_name=event_name).first()
        if db_event_name is not None:
            return jsonify({"message": f"The event {event_name} already exits."})

        # add a new venue if not already in DB
        db_venue = Venue.query.filter_by(name=venue_name).first()
        if db_venue is not None:  # if in DB
            venue_id = db_venue.venue_id
        else:
            new_venue = Venue(
                name=data.get('venue_name'),
                location=data.get('venue_location'),
                postcode=data.get('venue_postcode'),
                capacity=data.get('venue_capacity'),
            )
            new_venue.save()
            venue_id = new_venue.venue_id

        # add a new event
        new_event = Event(
            venue_id=venue_id,
            event_name=data.get('event_name'),
            datetime=datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M:%S'),
            genre=data.get('genre'),
            description=data.get('description'),
        )
        new_event.save()
        return jsonify({"message": f"Event {event_name} created successfully."})


# Delete an event by name, if it exists.
@api.route('/delete_event/<string:name>')
class DeleteEvent(Resource):  # HandleEvent class, retrieve/delete by name?
    @management_required
    def delete(self, name):
        event_to_delete = Event.query.filter_by(event_name=name).first()
        if event_to_delete:
            event_to_delete.delete()
            return jsonify({"success": True, "message": f"Event {name} deleted successfully."})
        return jsonify({"success": False, "message": f"Event {name} does not exist."})


# Get all events.
@api.route('/event_list')
class EventList(Resource):
    @jwt_required()
    def get(self):
        events = Event.query.all()
        response = []
        for event in events:
            data = {
                'event_name': event.event_name,
                'event_id': event.event_id,
                'datetime': str(event.datetime),
                'genre': event.genre,
                'description': event.description,
                'venue_name': event.venue.name,
                'venue_location': event.venue.location,
                'venue_postcode': event.venue.postcode,
                'venue_capacity': event.venue.capacity
            }
            response.append(data)
        return response


@api.route('/event/<int:event_id>')
class EventDetails(Resource):
    @jwt_required()
    def get(self, event_id):
        event = Event.query.filter_by(event_id=event_id).one_or_none()

        if event is None:
            return msg_response("Event does not exist", status_code=400)

        return jsonify({'event_name': event.event_name,
                        'event_id': event.event_id,
                        'datetime': str(event.datetime),
                        'genre': event.genre,
                        'description': event.description,
                        'venue_name': event.venue.name,
                        'venue_location': event.venue.location,
                        'venue_postcode': event.venue.postcode,
                        'venue_capacity': event.venue.capacity
                        })


@api.route('/event_search')
class EventSearch(Resource):
    @api.expect(search_event_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        query = data.get('event_name')

        events = Event.query.filter(Event.event_name.contains(query)).all()
        response = []
        for event in events:
            data = {
                'event_name': event.event_name,
                'event_id': event.event_id,
                'datetime': str(event.datetime),
                'genre': event.genre,
                'description': event.description,
                'venue_name': event.venue.name,
                'venue_location': event.venue.location,
                'venue_postcode': event.venue.postcode,
                'venue_capacity': event.venue.capacity
            }
            response.append(data)
        return response


@api.route('/addticket')
class AddTicketResource(Resource):
    @jwt_required()
    def get(self):
        retry = True
        while retry:
            # Generate and store new idepotency token
            token = utils.generate_token()
            newToken = IdempotencyTokens(token=token, valid=1)
            db.session.add(newToken)

            try:
                # Throw error if idempotency token already exists
                db.session.commit()
                retry = False
            except IntegrityError:
                # Token exists retry generation
                retry = True
            except:
                return jsonify({"msg", "Server Error"})

        return jsonify({"key": token})

    @api.expect(add_ticket_input_model)
    @jwt_required()
    def post(self):
        args = request.get_json()
        # Check if idempotency token exists in table before adding ticket   
        existing_code = IdempotencyTokens.query.filter_by(token=args.get("token")).one_or_none()
        event_data = Event.query.filter_by(event_id=args.get("event_id")).one_or_none()

        # Check code and user id
        if existing_code is None or existing_code.valid == 0:
            return msg_response("Invalid request", status_code=400)

        # Check event
        if event_data is None:
            return msg_response("Invalid event", status_code=400)

        # Remove token
        existing_code.delete()

        # Make new ticket
        new_ticket = UserTicket(
            event_id=args.get("event_id"),
            ticket_type=args.get("ticket_type"),
            user_id=current_user.user_id,
            cipher_key=utils.gen_key(),
            valid=True
        )
        new_ticket.save()

        return msg_response("Ticket successfully added")


@api.route('/requestQRdata')
class RequestQRDataResource(Resource):
    @api.expect(request_qr_data_model)
    @jwt_required()
    def post(self):
        args = request.get_json()

        # Use ticket_id to lookup ticket data
        user_ticket = db.session.query(UserTicket).filter_by(ticket_id=args.get("ticket_id")).one_or_none()

        # Check basic ticket details
        if user_ticket is None:
            # Ticket doesn't exist
            return msg_response("Invalid request", status_code=400)
        elif user_ticket.valid == 0:
            # Ticket is invalid
            return msg_response("Invalid token", status_code=400)
        elif user_ticket.user_id != current_user.user_id:
            # Ticket does not belong to user
            return msg_response("Unauthorised ticket", status_code=400)

        # Encrypt ticket_id with cipher key
        try:
            ciphertext, iv = utils.encrypt(user_ticket.ticket_id, user_ticket.cipher_key)
        except:
            return msg_response("Error generating QR data", status_code=400)

        return jsonify({"ticket_id": user_ticket.ticket_id, "qr_data": ciphertext + iv})


@api.route('/validateTicket')
class ValidateTicketResource(Resource):
    @api.expect(validate_ticket_model)
    @management_required
    def post(self):
        args = request.get_json()

        # Use ticketID to lookup ticket data
        user_ticket = db.session.query(UserTicket).filter_by(ticket_id=args.get("ticket_id")).first()

        # Check basic ticket details
        if user_ticket is None:
            # Ticket doesn't exist
            return msg_response("Ticket doesn't exist", status_code=400)
        elif user_ticket.valid == 0:
            # Ticket is already used
            return msg_response("Ticket already used", status_code=400)

        # Use cipherkey to decrypt ciphertext
        try:
            ciphertext = args.get("qr_data")
            cipher = ciphertext[:24]
            iv = ciphertext[24:]
            decrypt_ticket_id = int(utils.decrypt(cipher, iv, user_ticket.cipher_key))

        except:
            return msg_response("Invalid ticket", status_code=400)

        # Check ticketId's match
        if decrypt_ticket_id != args.get("ticket_id"):
            return msg_response("Invalid ticket", status_code=400)

        # Check received event against ticket event
        if user_ticket.event_id is not args.get("event_id"):
            return msg_response(f"Ticket is not valid for this event "
                                f"{user_ticket.event.event_name}", status_code=400)

        # Make ticket invalid
        user_ticket.valid = 0
        try:
            user_ticket.save()
        except:
            return msg_response("Server error", status_code=400)

        # Return confirmation data
        return jsonify({"ticket_type": user_ticket.ticket_type, "msg": "Ticket is valid"})


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
    # app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("certificate/cert.pem", "certificate/key.pem"))
