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
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, origins="http://localhost:3000")
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

# /addticket expected input model
addTicketInput = api.model(
    "AddTicket",
    {
        "userID": fields.Integer(required=True, min=0),
        "eventID": fields.Integer(required=True, min=0),
        "ticketTypeID": fields.Integer(required=True, min=0),
        "token": fields.String(required=True, max_length=128)
    }
)

# Request QR code data input model
requestQRdataModel = api.model(
    "RequestQRdata",
    {
        "ticketId": fields.Integer(min=0, required=True)
    }
)

# Validate Ticket input model
validateTicketModel = api.model(
    "ValidateTicket",
    {
        "eventID": fields.Integer(min=0, required=True),
        "ticketID": fields.Integer(min=0, required=True),
        "QRdata": fields.String(required=True)
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


# Generates a random 32-byte key
def gen_key():
    key = get_random_bytes(32)

    return key


# Encrypts plain_text using AES-256-CBC
def encrypt(plain_text, key):
    # Input validation on key
    if not isinstance(key, bytes) or not len(key) == 32:
        return TypeError

    # Input validation on plain_text
    if not isinstance(plain_text, int) or abs(plain_text) != plain_text or not len(str(plain_text)) <= 8:
        return TypeError

    # Pad plain text by adding leading zeros
    plain_text = str(plain_text)
    plain_text = (8 - len(plain_text)) * '0' + plain_text

    # Encode string as bytes
    plain_text = bytes(plain_text, encoding='utf8')

    # Encrypt plain_text
    cypher = AES.new(key, AES.MODE_CBC)
    cypher_text = cypher.encrypt(pad(plain_text, AES.block_size))

    # Decode from bytes to string
    cypher_text = b64encode(cypher_text).decode()
    iv = b64encode(cypher.iv).decode()

    return cypher_text, iv


# Decrypts cypher text
def decrypt(cypher_text, iv, key):
    # Input validation on cypher text
    if not isinstance(cypher_text, str) or not len(cypher_text) == 24:
        return TypeError

    # Input validation on iv
    if not isinstance(iv, str) or not len(iv) == 24:
        return TypeError

    # Input validation on key
    if not isinstance(key, bytes) or not len(key) == 32:
        return TypeError

    # Decode from string to bytes
    cypher_text = b64decode(cypher_text)
    iv = b64decode(iv)

    # Decrypt cypher_text
    cypher = AES.new(key, AES.MODE_CBC, iv=iv)
    plain_text = unpad(cypher.decrypt(cypher_text), AES.block_size)

    return plain_text


def login_user_response(user, data=None):
    """Adds user login with cookie to response"""
    if data is None:
        data = {}
    access_token = create_access_token(identity=user.user_id)
    data['token'] = access_token
    response = jsonify(data)
    set_access_cookies(response, access_token)
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
            response = jsonify({"success": False, "message": msg})
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

        response_data = {"success": True, "message": f"User {data.get('email_address')} created successfully."}
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
        return jsonify({"email": current_user.email_address,
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


# datetime format: "2022-03-11 20:00:00"
# @jwt_required


# @jwt_required
@api.route('/add_event')
class AddEvent(Resource):

    @api.expect(event_model)
    # @management_required
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


# Retrieve event by name/id.   need a route for this?


# Delete an event by name, if it exists.
@api.route('/delete_event/<string:name>')
class DeleteEvent(Resource):  # HandleEvent class, retrieve/delete by name?
    # @jwt_required()
    def delete(self, name):
        event_to_delete = Event.query.filter_by(event_name=name).first()
        if event_to_delete:
            event_to_delete.delete()
            return jsonify({"success": True, "message": f"Event {name} deleted successfully."})
        return jsonify({"success": False, "message": f"Event {name} does not exist."})


# Get all events.
@api.route('/event_list')
class EventList(Resource):
    def get(self):
        events = Event.query.all()
        response = []
        for event in events:
            venue = Venue.query.filter_by(venue_id=event.venue_id).first()
            data = {
                'event_name': event.event_name,
                'datetime': str(event.datetime),
                'genre': event.genre,
                'description': event.description,
                'venue_name': venue.name,
                'venue_location': venue.location,
                'venue_postcode': venue.postcode,
                'venue_capacity': venue.capacity
            }
            response.append(data)
        return response


@api.route('/addticket')
class AddTicketResource(Resource):
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
                retry=True
            except:
                return jsonify({"msg", "Server Error"})

        return jsonify({"key":token})
    
    @api.expect(addTicketInput)
    def post(self):
        args = request.get_json()
        # Check if idempotency token exists in table before adding ticket   
        existing_code = db.session.query(IdempotencyTokens).filter_by(token=args.get("token")).first()
        user_data = db.session.query(User).filter_by(user_id=args.get("userID")).first()
        event_data = db.session.query(Event).filter_by(event_id=args.get("eventID")).first()

        # Check code and user id
        if existing_code is None or user_data is None:
            return jsonify({"msg":"Invalid request"})
        else:
            # Check if token is still valid
            if existing_code.valid == 0:
                return jsonify({"msg":"Invalid token"})
        
        # Check EventID
        if event_data is None:
            return jsonify({"msg":"Invalid event"})
        
        # Set token to be invalid
        existing_code.valid = 0
        
        newticket = UserTicket(
            event_id=args.get("eventID"),
            ticket_type=args.get("ticket_type"),
            user_id=args.get("userID"),
            cipher_key="random", ## Update with chris code
            iv="random", ## update
            valid=1
        )
        db.session.add(newticket)
        db.session.commit()

        # Update new ticket and invalidate idepotency token
        print("Successfully commited to database")
        try:
            pass
            
        except:
            jsonify({"msg":"Error try again"})

        return jsonify({"msg": "Ticket sucessfully added"})

@api.route('/requestQRdata')
class requestQRdataResource(Resource):
    @api.expect(requestQRdataModel)
    def post(self):
        args = request.get_json()

        # Use ticketID to lookup ticket data    
        user_ticket = db.session.query(UserTicket).filter_by(ticket_id=args.get("ticketId")).first()

        # Check if ticket doesnt exist
        if user_ticket is None:
            return jsonify({"msg":"Invalid request"})
        else:
            # Check if ticket is invaild
            if user_ticket.valid == 0:
                return jsonify({"msg":"Invalid token"})
        
        # Encrypt ticketID with cipherkey
        # try:
        ciphertext = "123" # ciphertext = encrypt(data=user_ticket.ticket_id, cipherkey=user_ticket.cipher_key)
        # except encryptionerror:
        #     return jsonify({"msg": "Ticket error"})

        return jsonify({"ticketID": user_ticket.ticket_id, "QRdata": ciphertext})


@api.route('/validateTicket')
class validateTicketResource(Resource):
    @api.expect(validateTicketModel)
    def post(self):
        args = request.get_json()

        # Use ticketID to lookup ticket data
        try:
            user_ticket = db.session.query(UserTicket).filter_by(ticket_id=args.get("ticketID")).first()
            user_data = db.session.query(User).filter_by(user_id=user_ticket.user_id).first()
        except:
            return jsonify({"msg": "Server error"})

        # Check if ticket doesnt exist
        if user_ticket is None:
            return jsonify({"msg":"Invalid request"})
        else:
            # Check if ticket is invaild
            if user_ticket.valid == 0:
                return jsonify({"msg":"Invalid token"})
        
        # Check if user_data is retrieved
        if user_data is None:
            return jsonify({"msg": "Server error"})
        
        # Use cipherkey to decrypt ciphertext
        try:
            decrpyt_ticket_id = 0 # decrypt(args.get("QRdata"), ticket_id.get("cipher_key")) using decrypt function
        except:
            return jsonify({"msg": "Ticket invalid"})

        # Check ticketId's match
        # if decrpyt_ticket_id != args.get("ticketId"):
        #     return jsonify({"msg": "Invalid ticket"})
    
        # Check recieved_event against ticket event
        if not user_ticket.event_id is args.get("eventID"):
            return jsonify({"msg": "Event is invalid"})

        # Make ticket invalid
        user_ticket.valid = 0
        try:
            user_ticket.save()
        except:
            return jsonify({"msg", "Server error"})

        # Return confirmation data
        return jsonify({"ticket_type": user_ticket.ticket_type})


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
    # app.run(host="0.0.0.0", port=443, debug=True, ssl_context=("certificate/cert.pem", "certificate/key.pem" ))
