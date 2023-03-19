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

    def test_signup_invalid_phone_number(self):
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

    def test_signup_invalid_phone_number_2(self):
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
        self.assertEqual(400, response.json.get("msg"))

    def test_login(self):
        data = {
            "email_address": "test@test.com",
            "password": "test1234"
        }

        response = self.app.post('/user/login', data=json.dumps(data), content_type='application/json')

        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
