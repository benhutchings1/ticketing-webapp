import json
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import create_app, db
from models import User

app = create_app('config.TestConfig')


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()
            self.test_user = User(
                email_address='test@test.com',
                passwd_hash=generate_password_hash('test1234', method="sha256", salt_length=32),
                firstname='Test',
                surname='Test',
                date_of_birth=datetime.strptime('2000-01-01', "%Y-%m-%d").date(),
                postcode='AB12 3DC',
                phone_number=f'07123456789',
                role='user'
            )
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
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

    def test_signup_invalid_email(self):
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

    def test_signup_invalid_password(self):
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

    def test_signup_invalid_firstname(self):
        data = {
            "email_address": "random2@random.com",
            "password": "test1234",
            "firstname": "t"*100,
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "33445345"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"The firstname & surname must be 32 characters or less", response.json.get("msg"))

    def test_signup_invalid_dob(self):
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

    def test_signup_invalid_postcode(self):
        data = {
            "email_address": "random4@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "t"*100,
            "phone_number": "3445"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Postcode length must be 8 or less", response.json.get("msg"))

    def test_signup_invalid_phone_number_non_numeric(self):
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

    def test_signup_invalid_phone_number_long(self):
        data = {
            "email_address": "random5@random.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "1"*50
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Phone number must be 16 digits or less", response.json.get("msg"))

    def test_signup_duplicate_email(self):
        data = {
            "email_address": "test@test.com",
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

    def test_signup_duplicate_phone_number(self):
        data = {
            "email_address": "random6@test.com",
            "password": "test1234",
            "firstname": "test",
            "surname": "test",
            "date_of_birth": "2023-03-16",
            "postcode": "test1234",
            "phone_number": "07123456789"
        }

        response = self.app.post('/user/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(f"Another user has this {data.get('phone_number')} phone number", response.json.get("msg"))

    def test_login(self):
        data = {
            "email_address": "test@test.com",
            "password": "test1234"
        }

        response = self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

        self.assertEqual(200, response.status_code)

    def test_login_invalid(self):
        data = {
            "email_address": "wrong email",
            "password": "wrong password"
        }

        response = self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

        self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    unittest.main()
