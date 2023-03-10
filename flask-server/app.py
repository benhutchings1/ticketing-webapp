from functools import wraps

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import current_config
from models import User, Event, Venue, TokenBlocklist
from exts import db
# from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, \
    unset_jwt_cookies, get_jwt, get_jwt_identity, current_user, verify_jwt_in_request
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
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
        "email_address": fields.String(max_length=100),  # max_length=100
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
        "event_name":fields.String(max_length=100),
        "date":fields.Date(),
        "time":fields.String(20), # DateTime(format='%H:%M:%S'),
        "genre":fields.String(max_length=100),
        "description":fields.String(max_length=1000),
        "venue_id":fields.Integer(),
        "venue.name":fields.String(max_length=100),
        "venue.location":fields.String(max_length=200),
        "venue.postcode":fields.String(max_length=7),
        "venue.capacity":fields.Integer()
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

''' 
This route adds a new event
To do so, it also adds a new venue & a new artist if not already in DB
'''
#@jwt_required
@api.route('/add_event')
class AddEvent(Resource):

    @api.expect(event_model)
    #@management_required
    def post(self):
        
        data = request.get_json()
        event_name = data.get('event_name')
        venue_name = data.get('venue_name')
  
        # event already exists in database?
        db_event_name = Event.query.filter_by(event_name=event_name).first()
        if db_event_name is not None:
            return jsonify({"message" : f"The event {event_name} already exits."})

        # add a new venue if not already in DB
        db_venue = Venue.query.filter_by(name=venue_name).first()
        if db_venue is not None: # if in DB
            venue_id = db_venue.venue_id
        else:
            new_venue = Venue(
                name = data.get('venue_name'),
                location = data.get('venue_location'),
                postcode = data.get('venue_postcode'),
                capacity = data.get('venue_capacity'),
            )
            new_venue.save()
            venue_id = new_venue.venue_id
       
        # add a new event
        new_event = Event(
            venue_id = venue_id,
            event_name = data.get('event_name'),
            date = datetime.strptime(data.get('date'), "%Y-%m-%d").date(),
            time = data.get('time'), #datetime.strptime(data.get('time'), '%H:%M:%S').time(),
            genre = data.get('genre'),
            description = data.get('description'),
        )
        new_event.save()
        return jsonify({"message" : f"Event {event_name} created successsfully."})


# Retrieve event by name/id.   need a route for this?


# Delete an event by name.    id instead?
@api.route('/delete_event/<string:name>')
class DeleteEvent(Resource): # HandleEvent class, retrieve/delete by name?
    def delete(self, name):
        event_to_delete = Event.query.filter_by(event_name=name).first_or_404()
        event_to_delete.delete()
        return jsonify({"message" : f"Event {name} deleted successsfully."})

# Get all events.   Need fix: some of the values are returned as null
#                             while they're not null in DB
@api.route('/event_list')
class EventList(Resource):
    @api.marshal_list_with(event_model)
    def get(self):
        return Event.query.all()

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

        return jsonify({"key":token})
    
    @api.expect(addTicketInput)
    def post(self):
        args = request.get_json()
        # Check if idempotency token exists in table before adding ticket   
        existing_code = db.session.query(IdempotencyTokens).filter_by(token=args.get("token")).first()

        if existing_code is None:
            return jsonify({"msg":"Invalid request"})
        else:
            # Check if token is still valid
            if existing_code.valid == 0:
                return jsonify({"msg":"Invalid token"})
            
        # Set token to be invalid
        existing_code.valid = 0
        
        newticket = UserTickets(
            eventID=args.get("eventID"),
            ticketTypeID=args.get("ticketTypeID"),
            userID=args.get("userID"),
            cipherkey="random", ## Update with chris code
            valid = 1
        )
        db.session.add(newticket)

        # Update new ticket and invalidate idepotency token
        try:
            db.session.commit()
        except:
            jsonify({"msg":"Error try again"})

        return jsonify({"msg": "Ticket sucessfully added"})


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
