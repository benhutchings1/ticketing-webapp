from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

from models import Event, Venue
from utils.access_control import management_required
from utils.response import msg_response

ns = Namespace('/event')

# /add_event expected input
event_model = ns.model(
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
search_event_model = ns.model(
    "SearchEvent",
    {
        "event_name": fields.String(),
    }
)


@ns.route('/add')
class AddEvent(Resource):
    @ns.expect(event_model)
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
@ns.route('/delete/<string:name>')
class DeleteEvent(Resource):  # HandleEvent class, retrieve/delete by name?
    @management_required
    def delete(self, name):
        event_to_delete = Event.query.filter_by(event_name=name).first()
        if event_to_delete:
            event_to_delete.delete()
            return jsonify({"success": True, "message": f"Event {name} deleted successfully."})
        return jsonify({"success": False, "message": f"Event {name} does not exist."})


# Get all events.
@ns.route('/list')
class EventList(Resource):
    @jwt_required()
    def get(self):
        events = Event.query.filter(Event.datetime > datetime.now() - timedelta(hours=12)).all()
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


@ns.route('/<int:event_id>')
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


@ns.route('/search')
class EventSearch(Resource):
    @ns.expect(search_event_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        query = data.get('event_name')

        events = Event.query.filter(Event.event_name.contains(query),
                                    Event.datetime > datetime.now() - timedelta(hours=12)
                                    ).all()

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
