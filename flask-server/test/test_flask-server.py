import json
import unittest
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import create_app, db
from models import User, Venue, Event, UserTicket

app = create_app('config.TestConfig')

VALID_USER = {
    "email_address": "test@test.com",
    "password": "test1234",
    "firstname": "test",
    "surname": "test",
    "date_of_birth": "2023-03-16",
    "postcode": "test1234",
    "phone_number": "07123456789"
}

VALID_MANAGEMENT = {
    "email_address": "admin@test.com",
    "password": "test1234",
    "firstname": "test",
    "surname": "test",
    "date_of_birth": "2023-03-16",
    "postcode": "test1234",
    "phone_number": "07123456783"
}


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()
            self.test_user = User(
                email_address=VALID_USER.get('email_address'),
                passwd_hash=generate_password_hash(VALID_USER.get('password'), method="sha256", salt_length=32),
                firstname=VALID_USER.get('firstname'),
                surname=VALID_USER.get('surname'),
                date_of_birth=datetime.strptime(VALID_USER.get('date_of_birth'), "%Y-%m-%d").date(),
                postcode=VALID_USER.get('postcode'),
                phone_number=VALID_USER.get('phone_number'),
                role='user'
            )

            self.test_user2 = User(
                email_address="test2@test.com",
                passwd_hash=generate_password_hash("test1234", method="sha256", salt_length=32),
                firstname="Test",
                surname="Test",
                date_of_birth=datetime.strptime("2023-03-16", "%Y-%m-%d").date(),
                postcode="test1234",
                phone_number="1234",
                role='user'
            )

            self.test_management = User(
                email_address=VALID_MANAGEMENT.get('email_address'),
                passwd_hash=generate_password_hash(VALID_MANAGEMENT.get('password'), method="sha256", salt_length=32),
                firstname=VALID_MANAGEMENT.get('firstname'),
                surname=VALID_MANAGEMENT.get('surname'),
                date_of_birth=datetime.strptime(VALID_MANAGEMENT.get('date_of_birth'), "%Y-%m-%d").date(),
                postcode=VALID_MANAGEMENT.get('postcode'),
                phone_number=VALID_MANAGEMENT.get('phone_number'),
                role='management'
            )

            self.venue = Venue(
                name='Test',
                location='Test',
                postcode='Test',
                capacity='Test',
            )

            self.test_event = Event(
                venue=self.venue,
                event_name='Test event',
                datetime=datetime.now(),
                genre='Test',
                description='Test',
            )

            self.test_event2 = Event(
                venue=self.venue,
                event_name='Test event 2',
                datetime=datetime.now(),
                genre='Test',
                description='Test',
            )

            self.test_event_old = Event(
                venue=self.venue,
                event_name='Test event',
                datetime=datetime.now() - timedelta(hours=13),
                genre='Test',
                description='Test',
            )

            self.test_ticket1 = UserTicket(
                event=self.test_event,
                user=self.test_user,
                ticket_type="Standard",
                valid=True,
            )

            self.test_ticket2 = UserTicket(
                event=self.test_event,
                user=self.test_user,
                ticket_type="Standard",
                valid=True,
            )

            self.test_ticket_used = UserTicket(
                event=self.test_event,
                user=self.test_user,
                ticket_type="Standard",
                valid=False,
            )

            self.test_ticket_old = UserTicket(
                event=self.test_event_old,
                user=self.test_user,
                ticket_type="Standard",
                valid=True,
            )

            self.test_ticket_user2 = UserTicket(
                event=self.test_event,
                user=self.test_user2,
                ticket_type="Standard",
                valid=True,
            )

            db.session.add(self.test_user)
            db.session.add(self.test_user2)
            db.session.add(self.test_management)
            db.session.add(self.venue)
            db.session.add(self.test_event)
            db.session.add(self.test_event2)
            db.session.add(self.test_event_old)
            db.session.add(self.test_ticket1)
            db.session.add(self.test_ticket2)
            db.session.add(self.test_ticket_used)
            db.session.add(self.test_ticket_user2)
            db.session.add(self.test_ticket_old)
            db.session.commit()

            self.test_event_id = self.test_event.event_id
            self.test_event2_id = self.test_event2.event_id
            self.test_event_old_id = self.test_event_old.event_id
            self.test_ticket_id = self.test_ticket1.ticket_id
            self.test_ticket_used_id = self.test_ticket_used.ticket_id
            self.test_ticket_user2_id = self.test_ticket_user2.ticket_id
            self.test_ticket_old_id = self.test_ticket_old.ticket_id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login_user(self):
        data = {
            "email_address": VALID_USER.get('email_address'),
            "password": VALID_USER.get('password')
        }

        self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

    def login_management(self):
        data = {
            "email_address": VALID_MANAGEMENT.get('email_address'),
            "password": VALID_MANAGEMENT.get('password')
        }

        self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

    def test_user_signup(self):
        data = {
            "email_address": "random@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "345345"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(200, response.status_code)

    def test_user_signup_invalid_email(self):
        data = {
            "email_address": "noemail",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "34544345"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"{data.get('email_address')}: invalid email address format", response.json.get("msg"))

    def test_user_signup_invalid_password(self):
        data = {
            "email_address": "random1@random.com",
            "password": "test",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "343445345"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Password length must be 8 or less", response.json.get("msg"))

    def test_user_signup_invalid_firstname(self):
        data = {
            "email_address": "random2@random.com",
            "password": "test1234",
            "firstname": "t" * 100,
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "33445345"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"The firstname & surname must be 32 characters or less", response.json.get("msg"))

    def test_user_signup_invalid_dob(self):
        data = {
            "email_address": "random3@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023",
            "postcode": "test1234",
            "phone_number": "345345223"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Date of birth must be valid", response.json.get("msg"))

    def test_user_signup_invalid_postcode(self):
        data = {
            "email_address": "random4@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "t" * 100,
            "phone_number": "3445"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Postcode length must be 8 or more", response.json.get("msg"))

    def test_user_signup_invalid_phone_number_non_numeric(self):
        data = {
            "email_address": "random5@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "no"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Phone number must be numeric", response.json.get("msg"))

    def test_user_signup_invalid_phone_number_long(self):
        data = {
            "email_address": "random5@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "1" * 50
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Phone number must be 16 digits or less", response.json.get("msg"))

    def test_user_signup_duplicate_email(self):
        data = {
            "email_address": VALID_USER.get('email_address'),
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "123456641"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"{data.get('email_address')} already has an account", response.json.get("msg"))

    def test_user_signup_duplicate_phone_number(self):
        data = {
            "email_address": "random6@test.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": VALID_USER.get('phone_number')
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Another user has this {data.get('phone_number')} phone number", response.json.get("msg"))

    def test_user_login(self):
        data = {
            "email_address": VALID_USER.get('email_address'),
            "password": VALID_USER.get('password')
        }

        response = self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

        self.assertEqual(200, response.status_code)

    def test_user_login_invalid(self):
        data = {
            "email_address": "wrong email",
            "password": "wrong password"
        }

        response = self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

        self.assertEqual(401, response.status_code)

    def test_ticket_add(self):
        self.login_user()

        response = self.app.get('/ticket/add')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json.get('key'))

        token = response.json.get('key')
        data = {
            "event_id": self.test_event_id,
            "ticket_type": "Standard",
            "ticket_quantity": 1,
            "token": token,
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual("1 ticket(s) successfully added", response.json.get('msg'))

    def test_ticket_add_invalid_event(self):
        self.login_user()

        response = self.app.get('/ticket/add')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json.get('key'))

        token = response.json.get('key')
        data = {
            "event_id": 1000000,
            "ticket_type": "Standard",
            "ticket_quantity": 1,
            "token": token,
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid event", response.json.get('msg'))

    def test_ticket_add_invalid_ticket_type(self):
        self.login_user()

        response = self.app.get('/ticket/add')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json.get('key'))

        token = response.json.get('key')
        data = {
            "event_id": self.test_event_id,
            "ticket_type": "invalid",
            "ticket_quantity": 1,
            "token": token,
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid ticket type", response.json.get('msg'))

    def test_ticket_add_invalid_quantity_small(self):
        self.login_user()

        response = self.app.get('/ticket/add')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json.get('key'))

        token = response.json.get('key')
        data = {
            "event_id": self.test_event_id,
            "ticket_type": "Standard",
            "ticket_quantity": -10,
            "token": token,
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid request", response.json.get('msg'))

    def test_ticket_add_invalid_quantity_large(self):
        self.login_user()

        response = self.app.get('/ticket/add')
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json.get('key'))

        token = response.json.get('key')
        data = {
            "event_id": self.test_event_id,
            "ticket_type": "Standard",
            "ticket_quantity": 1000,
            "token": token,
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid request", response.json.get('msg'))

    def test_ticket_add_invalid_token(self):
        self.login_user()

        data = {
            "event_id": self.test_event_id,
            "ticket_type": "Standard",
            "ticket_quantity": 1,
            "token": "invalid",
        }

        response = self.app.post('/ticket/add', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual("Invalid request", response.json.get('msg'))

    def test_ticket_list(self):
        self.login_user()

        response = self.app.get('/ticket/list')
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json))

    def test_ticket_qr_data(self):
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_ticket_qr_data_non_existent_ticket(self):
        self.login_user()

        data = {
            "ticket_id": 1000000
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_qr_data_used_ticket(self):
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_used_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_qr_data_unauthorised_ticket(self):
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_user2_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(401, response.status_code)

    def test_ticket_qr_data_old_ticket(self):
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_old_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_ticket_validate_old_session(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        self.login_user()

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_invalid_event(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": 1000000000,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_ticket_validate_invalid_structure(self):
        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": "ticket"
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_invalid_structure_ints(self):
        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": "t,t,t,hash,sign"
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_invalid_signature(self):
        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": f"{self.test_ticket_id},{self.test_ticket1.event_id},0,hash,signature"
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_modified_ticket_type(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Modification
        qr_data_elements = qr_data.split(",")
        qr_data_elements[2] = "1"
        qr_data = ",".join(qr_data_elements)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_modified_event_id(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Modification
        qr_data_elements = qr_data.split(",")
        qr_data_elements[1] = f"{self.test_event2_id}"
        qr_data = ",".join(qr_data_elements)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_event2_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_modified_ticket_id(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Modification
        qr_data_elements = qr_data.split(",")
        qr_data_elements[0] = f"{self.test_ticket_user2_id}"
        qr_data = ",".join(qr_data_elements)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_event_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_used_ticket(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": qr_data
        }

        for i in range(2):
            response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_previous_qr_code(self):
        # Get qr code
        self.login_user()

        data = {
            "ticket_id": self.test_ticket_id
        }

        # Generate 1st time
        response = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data = response.json.get('qr_data')
        self.assertIsNotNone(qr_data)

        # Generate 2nd time
        response2 = self.app.post('/ticket/request_qr_data', data=json.dumps(data), content_type='application/json')
        qr_data2 = response2.json.get('qr_data')
        self.assertIsNotNone(qr_data2)

        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_ticket1.event_id,
            "qr_data": qr_data
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_ticket_validate_old_event(self):
        # Verify qr code
        self.login_management()

        data = {
            "event_id": self.test_event_old_id,
            "qr_data": "qr_data"
        }

        response = self.app.post('/ticket/validate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
