from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource, fields, Namespace

from exts import db
from models import UserTicket
from utils.access_control import management_required
from utils.encryption import encrypt, decrypt
from utils.response import msg_response

ns = Namespace('/ticket_no_sign')

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


@ns.route('/request_qr_data')
class RequestQRDataResource(Resource):
    @ns.expect(request_qr_data_model)
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
