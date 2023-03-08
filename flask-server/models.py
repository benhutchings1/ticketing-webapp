from exts import db

# user table
class UserTable(db.Model):
    userId = db.Column(db.Integer(), primary_key=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    surName = db.Column(db.String(20), nullable=False)
    #dateOfBirth = db.Column(db.Date, nullable=False)
    #postCode = db.Column(db.String(6), nullable=False)
    #phoneNumber = db.Column(db.String(10), nullable=False)
    emailAddress = db.Column(db.String(100), nullable=False)
    #role = db.Column(db.Text(), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, userId, firstName, surName, dateOfBirth, postCode, phoneNumber, emailAddress, role):
        self.title = userId
        self.firstName = firstName
        self.surName = surName
        self.dateOfBirth = dateOfBirth
        self.postCode = postCode
        self.phoneNumber = phoneNumber
        self.phoneNumber = phoneNumber
        self.role = role
        db.session.commit()

'''

# event table
class EventTable(db.Model):
    eventId = db.Column(db.Integer(), primary_key=True ,nullable=False)
    eventName = db.Column(db.String(), nullable=False)
    venueId = db.Column(db.Integer(), nullable=False) # or venue object or type Venue?
    date = db.Column(db.Date, nullable=False)
    #time = db.Column(db.Time, nullable=False, default=time(0, 0))
    artistId = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text(800), nullable=False)

    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, eventId, eventName, venueId, date, time, artistId, description ):
        self.eventId = eventId
        self.eventName = eventName
        self.venueId = venueId
        self.time = time
        self.artistId = artistId
        self.description = description
        db.session.commit()



# tickets table
class TicketTable(db.Model):
    ticketTypeId = db.Column(db.Integer(), primary_key=True ,nullable=False)
    eventId = db.Column(db.Integer(), primary_key=True ,nullable=False)
    ticketName = db.Column(db.String(), nullable=False)
    ticketDescription = db.Column(db.Text(800), nullable=False)

    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, ticketTypeId, eventId, ticketName, ticketDescription ):
        self.ticketTypeId = ticketTypeId
        self.eventId = eventId
        self.ticketName = ticketName
        self.ticketDescription = ticketDescription
        db.session.commit()



# venue table
class VenueTable(db.Model):
    venueId = db.Column(db.Integer(), primary_key=True ,nullable=False)
    location = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    postCode = db.Column(db.String(6), nullable=False)
    capacity = db.Column(db.Integer(), nullable=True)
    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, venueId, name, postCode, capacity ):
        self.venueId = venueId
        self.name = name
        self.postCode = postCode
        self.capacity = capacity
        db.session.commit()



# artist table
class ArtistTable(db.Model):
    artistId = db.Column(db.Integer(), primary_key=True, nullable=False)
    artistFirstName = db.Column(db.String(), nullable=False)
    artistSurName = db.Column(db.String(), nullable=False)


    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, artistFirstName, artistSurName):
        self.artistFirstName = artistFirstName
        self.artistSurName = artistSurName
        db.session.commit()



# user ticket table
class UserTicketTable(db.Model):
    ticketId = db.Column(db.Integer(), primary_key=True ,nullable=False)
    eventId = db.Column(db.Integer(),nullable=False)
    userId = db.Column(db.Integer(), nullable=False)
    cipherkey = db.Column(db.String(), nullable=False)
    ticketTypeId = db.Column(db.Integer(), nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    db.session.commit()

    #def __repr__(self):
    #    pass
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, ticketId, eventId, userId, cipherkey, ticketTypeId, valid ):
        self.ticketId = ticketId
        self.eventId = eventId
        self.userId = userId
        self.cipherkey = cipherkey
        self.ticketTypeId = ticketTypeId
        self.valid = valid
        db.session.commit()
'''