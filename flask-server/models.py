from exts import db


# User model
class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    date_of_birth = db.Column(db.Date)
    postcode = db.Column(db.String(8))
    phone_number = db.Column(db.String(16), unique=True)
    email_address = db.Column(db.String(64), nullable=False, unique=True)
    role = db.Column(db.String(16), nullable=False)
    passwd_hash = db.Column(db.String(256), nullable=False)

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


# Event and ticket models
class Event(db.Model):
    event_id = db.Column(db.Integer(8), primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(128), nullable=False)
    venue_id = db.Column(db.Integer(8), db.ForeignKey('venue.venue_id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)  # I have set this to datetime but can be changed if needed
    description = db.Column(db.Text)  # db.Text() . Overflow?
    genre = db.Column(db.String(128))
    venue = db.relationship("Venue")

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

# Venue model
class Venue(db.Model):
    venue_id = db.Column(db.Integer(8), primary_key=True, autoincrement=True)
    location = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    postcode = db.Column(db.String(8), nullable=False)
    capacity = db.Column(db.Integer(8))

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


# model for tickets to be generated for specific user
class UserTicket(db.Model):
    ticket_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.event_id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    cipher_key = db.Column(db.String(256), nullable=False)
    ticket_type = db.Column(db.String(64), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)

    event = db.relationship("Event")
    user = db.relationship("User")

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


class IdempotencyTokens(db.Model):
    token = db.Column(db.String(128), primary_key=True, index=True)
    valid = db.Column(db.Integer(1))
