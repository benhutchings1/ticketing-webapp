from app import create_app
from exts import db
from models import User, Venue, Event
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Test users will have default password 'test'
TEST_USERS = [
    {'email': 'test@test.com', 'role': 'user'},
    {'email': 'test1@test.com', 'role': 'user'},
    {'email': 'admin@test.com', 'role': 'management'},
]

# Test venues will alternate between events
TEST_VENUES = [
    {'name': 'Stadium', 'location': 'City', 'capacity': 10000},
    {'name': 'Room', 'location': 'City', 'capacity': 5000},
]

# Test events will be created with a date and time relative to current time
TEST_EVENTS = [
    {'name': 'Party Time', 'datetime': timedelta(hours=2), 'genre': 'Party'},
    {'name': 'Music Time', 'datetime': timedelta(days=3), 'genre': 'Music'},
    {'name': 'Football Time', 'datetime': timedelta(days=7), 'genre': 'Sport'},
    {'name': 'Dance Time', 'datetime': timedelta(days=28), 'genre': 'Dance'},
    {'name': 'Food Time', 'datetime': timedelta(days=365), 'genre': 'Food'},
    {'name': 'Rugby Time', 'datetime': timedelta(days=-3), 'genre': 'Sport'},
]

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        # Delete contents of db and recreate
        db.drop_all()
        db.create_all()

        # Create test users
        for i, data in enumerate(TEST_USERS):
            test_user = User(
                email_address=data.get('email'),
                passwd_hash=generate_password_hash('test', method="sha256", salt_length=32),
                firstname='Test',
                surname='Test',
                date_of_birth=datetime.strptime('2000-01-01', "%Y-%m-%d").date(),
                postcode='AB12 3DC',
                phone_number=f'07345345{i}',
                role=data.get('role')
            )
            test_user.save()

        # Create test venues
        test_venues = []
        for i, data in enumerate(TEST_VENUES):
            test_venue = Venue(
                name=data.get('name'),
                location=data.get('location'),
                postcode='AB12 3DC',
                capacity=data.get('capacity'),
            )
            test_venue.save()
            test_venues.append(test_venue)

        # Create test events
        for i, data in enumerate(TEST_EVENTS):
            # Calculate date for event
            event_datetime = datetime.now() + data.get('datetime')
            event_venue = test_venues[i % 2]

            # Create event
            test_event = Event(
                venue=event_venue,
                event_name=data.get('name'),
                datetime=event_datetime,
                genre=data.get('genre'),
                description=f"{data.get('name')} is at {event_venue.name} on "
                            f"{event_datetime.strftime('%A %d %B, %Y @ %H:%M')}",
            )
            test_event.save()
