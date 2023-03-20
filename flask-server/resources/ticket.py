import binascii
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from xxhash import xxh32

from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource, fields, Namespace
from sqlalchemy.exc import IntegrityError

from exts import db
from models import IdempotencyTokens, Event, UserTicket
from utils.access_control import management_required
from utils.encryption import generate_token, gen_key
from utils.response import msg_response
from utils.signature import create_key_pair, verify_msg, sign_msg

# Valid ticket types
TICKET_TYPES = ["Standard", "Deluxe", "VIP"]

# Signature
public_key, private_key = create_key_pair()

ns = Namespace('/ticket')

# /addticket expected input model
add_ticket_input_model = ns.model(
    "AddTicket",
    {
        "event_id": fields.Integer(required=True, min=0),
        "ticket_type": fields.String(required=True),
        "ticket_quantity": fields.Integer(required=True),
        "token": fields.String(required=True, max_length=128),
    }
)

# Request QR code data input model
request_qr_data_model = ns.model(
    "RequestQRdata",
    {
        "ticket_id": fields.Integer(min=0, required=True)
    }
)

# Validate Ticket input model with signature
validate_ticket_model = ns.model(
    "ValidateTicket",
    {
        "event_id": fields.Integer(min=0, required=True),
        "qr_data": fields.String(required=True)
    }
)

# Tickets
ticket_model = ns.model(
    "Ticket",
    {
        "ticket_id": fields.Integer(attribute="ticket_id"),
        "event_id": fields.Integer(attribute="event.event_id"),
        "event_name": fields.String(attribute="event.event_name"),
        "event_datetime": fields.String(attribute="event.datetime"),
        "venue_id": fields.String(attribute="event.venue.venue_id"),
        "venue_name": fields.String(attribute="event.venue.name"),
        "venue_location": fields.String(attribute="event.venue.location"),
        "venue_postcode": fields.String(attribute="event.venue.postcode"),
        "venue_capacity": fields.String(attribute="event.venue.capacity")
    }
)


@ns.route('/list')
class TicketList(Resource):
    @jwt_required()
    @ns.marshal_list_with(ticket_model)
    def get(self):
        return UserTicket.query.join(Event) \
            .filter(UserTicket.user == current_user,
                    UserTicket.valid,
                    Event.datetime > datetime.now() - timedelta(hours=12)
                    ).all()


@ns.route('/add')
class AddTicketResource(Resource):
    @jwt_required()
    def get(self):
        retry = True
        while retry:
            # Generate and store new idepotency token
            token = generate_token()
            new_token = IdempotencyTokens(token=token, valid=1)
            db.session.add(new_token)

            try:
                # Throw error if idempotency token already exists
                db.session.commit()
                retry = False
            except IntegrityError:
                # Token exists retry generation
                retry = True
            except:
                return msg_response("Server Error", status_code=400)

        return jsonify({"key": token})

    @ns.expect(add_ticket_input_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        # Check if idempotency token exists in table before adding ticket
        existing_code = IdempotencyTokens.query.filter_by(token=data.get("token")).one_or_none()
        event = Event.query.filter(Event.event_id == data.get("event_id"),
                                   Event.datetime > datetime.now() - timedelta(hours=12)).one_or_none()

        # Check code and user id
        if existing_code is None or existing_code.valid == 0:
            return msg_response("Invalid request", status_code=400)

        # Remove token
        existing_code.delete()

        # Check event
        if event is None:
            return msg_response("Invalid event", status_code=400)

        # Check ticket type
        if data.get("ticket_type") not in TICKET_TYPES:
            return msg_response("Invalid ticket type", status_code=400)

        # Check number of tickets is allowed
        if not (0 < data.get("ticket_quantity") <= 4):
            return msg_response("Invalid request", status_code=400)

        # Add new tickets
        for i in range(data.get("ticket_quantity")):
            new_ticket = UserTicket(
                event_id=data.get("event_id"),
                ticket_type=data.get("ticket_type"),
                user_id=current_user.user_id,
                valid=True
            )
            new_ticket.save()

        return msg_response(f"{data.get('ticket_quantity')} ticket(s) successfully added")


@ns.route('/request_qr_data')
class RequestQRDataResource(Resource):
    @ns.expect(request_qr_data_model)
    @jwt_required()
    def post(self):
        data = request.get_json()

        # Use ticket_id to lookup ticket data
        user_ticket = UserTicket.query.get(data.get("ticket_id"))

        # Check basic ticket details
        if user_ticket is None:
            # Ticket doesn't exist
            return msg_response("Ticket does not exist", status_code=400)
        elif user_ticket.valid == 0:
            # Ticket is invalid
            return msg_response("Ticket already used", status_code=400)
        elif user_ticket.user_id != current_user.user_id:
            # Ticket does not belong to user
            return msg_response("Unauthorised ticket", status_code=401)
        elif user_ticket.event.datetime <= datetime.now() - timedelta(hours=12):
            # Event has already happened
            return msg_response("Event is over", status_code=400)

        # Get ticket type as int
        try:
            ticket_type_int = TICKET_TYPES.index(user_ticket.ticket_type)
        except ValueError:
            # Ticket is corrupt
            return msg_response("Ticket is corrupt", status_code=400)

        # Update ticket salt
        user_ticket.salt = gen_key()
        user_ticket.update()

        # Generate hash for session
        session_hash = xxh32(f"{current_user.jti}{user_ticket.salt}").hexdigest()

        # Ticket details as plaintext
        details = f"{user_ticket.ticket_id},{user_ticket.event_id},{ticket_type_int},{session_hash}"
        details_bytes = details.encode()

        # Sign ticket details with private key
        signature_bytes = sign_msg(details_bytes, private_key)
        signature = b64encode(signature_bytes).decode()

        # QR Code data
        qr_data = f"{details},{signature}"

        return jsonify({"ticket_id": user_ticket.ticket_id, "qr_data": qr_data})


@ns.route('/validate')
class ValidateTicketResource(Resource):
    @ns.expect(validate_ticket_model)
    @management_required
    def post(self):
        data = request.get_json()

        # Check event exists and has not finished
        event = Event.query.get(data.get('event_id'))
        if event is None:
            return msg_response("Event does not exist", status_code=404)
        elif event.datetime <= datetime.now() - timedelta(hours=12):
            return msg_response("Event is over", status_code=400)

        # QR Code data
        qr_data = data.get('qr_data')
        qr_data_structure = qr_data.split(",")

        # Validation of structure
        if len(qr_data_structure) != 5 or False in [i.isdecimal() for i in qr_data_structure[0:3]]:
            return msg_response("Ticket is invalid", status_code=400)

        # Get ticket details
        ticket_id = int(qr_data_structure[0])
        event_id = int(qr_data_structure[1])
        ticket_type_int = int(qr_data_structure[2])
        session_hash = qr_data_structure[3]

        # Check ticket event matches current event
        if event_id != data.get('event_id'):
            return msg_response("Ticket doesn't match event", status_code=400)

        # Get original msg
        msg = f"{ticket_id},{event_id},{ticket_type_int},{session_hash}"
        msg_bytes = msg.encode()

        # Get signature
        signature = qr_data_structure[4]
        try:
            signature_bytes = b64decode(signature)
        except binascii.Error:
            return msg_response("Ticket is invalid", status_code=400)

        # Verify signature
        valid = verify_msg(msg_bytes, signature_bytes, public_key)
        if not valid:
            return msg_response("Ticket is invalid", status_code=400)

        # Fetch ticket from database
        user_ticket = UserTicket.query.get(ticket_id)

        # Check basic ticket details
        if user_ticket is None:
            # Ticket was deleted
            return msg_response("Ticket was deleted", status_code=400)
        elif user_ticket.valid == 0:
            # Ticket is already used
            return msg_response("Ticket already used", status_code=400)

        # Check hash
        current_hash = xxh32(f"{user_ticket.user.jti}{user_ticket.salt}").hexdigest()
        if current_hash != session_hash:
            # Ticket is outdated
            return msg_response("Ticket is outdated", status_code=400)

        # Set ticket as used
        user_ticket.valid = 0
        user_ticket.save()

        # Return confirmation data
        return jsonify({"ticket_type": user_ticket.ticket_type, "msg": "Ticket is valid"})
