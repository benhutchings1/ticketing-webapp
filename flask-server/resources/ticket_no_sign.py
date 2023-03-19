from datetime import datetime, timedelta

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource, fields, Namespace
from sqlalchemy.exc import IntegrityError

from exts import db
from models import Base, IdempotencyTokens, Event
from utils.access_control import management_required
from utils.encryption import encrypt, decrypt, generate_token, gen_key
from utils.response import msg_response

ns = Namespace('/ticket_no_sign')

# Valid ticket types
TICKET_TYPES = ["Standard", "Deluxe", "VIP"]


# User ticket no sign model
class UserTicketNoSign(Base):
    ticket_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.event_id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    cipher_key = db.Column(db.String(256), nullable=False)
    ticket_type = db.Column(db.String(64), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)

    event = db.relationship("Event")
    user = db.relationship("User")


# Validate Ticket input model without signature
validate_ticket_model_no_sign = ns.model(
    "ValidateTicket",
    {
        "event_id": fields.Integer(min=0, required=True),
        "ticket_id": fields.Integer(min=0, required=True),
        "qr_data": fields.String(required=True)
    }
)

# Request QR code data input model
request_qr_data_model = ns.model(
    "RequestQRdata",
    {
        "ticket_id": fields.Integer(min=0, required=True)
    }
)

add_ticket_input_model = ns.model(
    "AddTicket",
    {
        "event_id": fields.Integer(required=True, min=0),
        "ticket_type": fields.String(required=True),
        "token": fields.String(required=True, max_length=128)
    }
)


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

        # Check event
        if event is None:
            return msg_response("Invalid event", status_code=400)

        # Check ticket type
        if data.get("ticket_type") not in TICKET_TYPES:
            return msg_response("Invalid ticket type", status_code=400)

        # Remove token
        existing_code.delete()

        # Make new ticket
        new_ticket = UserTicketNoSign(
            event_id=data.get("event_id"),
            ticket_type=data.get("ticket_type"),
            user_id=current_user.user_id,
            cipher_key=gen_key(),
            valid=True
        )
        new_ticket.save()

        return msg_response("Ticket successfully added")


@ns.route('/request_qr_data')
class RequestQRDataResource(Resource):
    @ns.expect(request_qr_data_model)
    @jwt_required()
    def post(self):
        args = request.get_json()

        # Use ticket_id to lookup ticket data
        user_ticket = db.session.query(UserTicketNoSign).filter_by(ticket_id=args.get("ticket_id")).one_or_none()

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
            ciphertext, iv = encrypt(user_ticket.ticket_id, user_ticket.cipher_key)
        except:
            return msg_response("Error generating QR data", status_code=400)

        return jsonify({"ticket_id": user_ticket.ticket_id, "qr_data": ciphertext + iv})


@ns.route('/validate')
class ValidateTicketResource(Resource):
    @ns.expect(validate_ticket_model_no_sign)
    @management_required
    def post(self):
        args = request.get_json()

        # Use ticketID to lookup ticket data
        user_ticket = db.session.query(UserTicketNoSign).filter_by(ticket_id=args.get("ticket_id")).first()

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
            decrypt_ticket_id = int(decrypt(cipher, iv, user_ticket.cipher_key))

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
