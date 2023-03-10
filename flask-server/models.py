from exts import db


# User model
class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    passwd_hash = db.Column(db.String(16), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date)
    postcode = db.Column(db.String(7))
    phone_number = db.Column(db.String(14), unique=True)
    role = db.Column(db.String(100), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, email_address, passwd_hash, postcode, phone_number):
        self.email_address = email_address
        self.passwd_hash = passwd_hash
        self.postcode = postcode
        self.phone_number = phone_number
        db.session.commit()


# Venue model
class Venue(db.Model):
    venue_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    postcode = db.Column(db.String(7), nullable=False)
    capacity = db.Column(db.Integer())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, name, location, postcode, capacity):
        self.name = name
        self.location = location
        self.postcode = postcode
        self.capacity = capacity
        db.session.commit()


# Artist model
class Artist(db.Model):
    artist_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, firstname, surname):
        self.firstname = firstname
        self.surname = surname
        db.session.commit()


# Event model
class Event(db.Model):
    event_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.venue_id'), nullable=False)
    artist_id = db.Column(db.Integer(), db.ForeignKey('venue.venue_id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20)) #db.Column(db.Time, nullable=False)   string is easier to marshal/jsonify
    genre = db.Column(db.String(100))
    description = db.Column(db.String(1000))  # db.Text() . Overflow?

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, event_name, date, time, genre, description):
        self.event_name = event_name
        self.date = date
        self.time = time
        self.genre = genre
        self.description = description
        db.session.commit()


# model for info about ticket types
class EventTicket(db.Model):
    ticket_type_id = db.Column(db.Integer(), primary_key=True)  # autoincrement=True, not supported with joint pk
    event_id = db.Column(db.Integer(), db.ForeignKey('event.event_id'), primary_key=True)
    ticket_name = db.Column(db.String(40), nullable=False)
    ticket_description = db.Column(db.String(1000), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, ticket_name, ticket_description):
        self.ticket_name = ticket_name
        self.ticket_description = ticket_description
        db.session.commit()


# model for tickets to be generated for specific user
class UserTicket(db.Model):
    ticket_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.event_id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    ticket_type_id = db.Column(db.Integer(), db.ForeignKey('event_ticket.ticket_type_id'), nullable=False)
    cipher_key = db.Column(db.String(), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
