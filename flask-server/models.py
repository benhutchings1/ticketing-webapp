from exts import db


class Base(db.Model):
    __abstract__ = True

    def save(self):
        """Adds the object to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the object from database"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """Commits changes to database"""
        db.session.commit()


class User(Base):
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    date_of_birth = db.Column(db.Date)
    postcode = db.Column(db.String(8))
    phone_number = db.Column(db.String(16), unique=True)
    email_address = db.Column(db.String(64), nullable=False, unique=True)
    role = db.Column(db.String(16), nullable=False)
    passwd_hash = db.Column(db.String(256), nullable=False)


class Event(Base):
    event_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(128), nullable=False)
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.venue_id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(128))

    venue = db.relationship("Venue")


class Venue(Base):
    venue_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    location = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    postcode = db.Column(db.String(8), nullable=False)
    capacity = db.Column(db.Integer())


class UserTicket(Base):
    ticket_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('event.event_id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    cipher_key = db.Column(db.String(256), nullable=False)
    ticket_type = db.Column(db.String(64), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)

    event = db.relationship("Event")
    user = db.relationship("User")


class TokenBlocklist(Base):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


class IdempotencyTokens(Base):
    token = db.Column(db.String(128), primary_key=True, index=True)
    valid = db.Column(db.Integer())
