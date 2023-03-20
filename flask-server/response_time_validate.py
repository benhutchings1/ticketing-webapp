import json
from datetime import datetime
from werkzeug.security import generate_password_hash
#Wfrom app import create_app, db
from app import *
from resources import *
from models import User
import time
import matplotlib.pyplot as plt
import numpy as np

app = create_app('config.TestConfig')

client = app.test_client()

def setUp():
    with app.app_context():
        tearDown()
        db.create_all()
        test_user = User(
            email_address='test@test.com',
            passwd_hash=generate_password_hash('test1234', method="sha256", salt_length=32),
            firstname='Test',
            surname='Test',
            date_of_birth=datetime.strptime('2000-01-01', "%Y-%m-%d").date(),
            postcode='AB12 3DC',
            phone_number=f'07345345',
            role='management' #role='user'
        )
        db.session.add(test_user)
        db.session.commit()

def tearDown():
    with app.app_context():
        db.session.remove()
        db.drop_all()

def singup_and_login():
    data = {
        "email_address": "random@random.com",
        "password": "test1234",
        "firstname": "test",
        "surname": "test",
        "date_of_birth": "2023-03-16",
        "postcode": "test1234",
        "phone_number": "345345"
    }
    login_data = {
            "email_address": "test@test.com",
            "password": "test1234"
        }
    signup_response = client.post('/user/signup', data=json.dumps(data), content_type='application/json')
    login_response = client.post('/user/login', data=json.dumps(login_data), content_type='application/json')

    return login_response



def reponse_time():
    ''' This method measures the reponse time of an endpoint in milliseconds
        Here, it is being used with /account route
        but it is meant to measure the reponse time of
        /addticket
        /requestQRdata
        /validateTicket
    '''
    
    response_times = []
    for i in range(1000):

        setUp()

        access_token = singup_and_login().json['token']
        headers = {'Authorization': f'Bearer {access_token}'}


        # add event
        event_data = {
            "event_name": "Party Timeeee",
            "datetime": "2023-03-09 12:10:00",
            "genre": "some genre",
            "description": "none",
            "venue_name": "venue1",
            "venue_location": "location",
            "venue_postcode": "postcode",
            "venue_capacity": 1000
            }

        add_event_response = client.post('/event/add', data=json.dumps(event_data), content_type='application/json', headers=headers)
        #print(add_event_response.data)
        
        # Get request
        key = client.get('/ticket/add', headers=headers)
        ticket_data = {
            "event_id": 1,
            "ticket_type": "Standard",
            "token": key.json['key']
        }
        # Post request
        response = client.post('/ticket/add', headers=headers, data=json.dumps(ticket_data), content_type='application/json')
        #print(response.data) 

        qr_data = {
            "ticket_id": 1
            }
        qr_response = client.post('/ticket/request_qr_data', headers=headers, data=json.dumps(qr_data), content_type='application/json')
        #print(qr_response.data)


        time0 = time.time() # start time
        validate_data = {
            "event_id": 1,
            "ticket_id": 1,
            "qr_data": str(qr_response.json['qr_data'])
            }
        validate_response = client.post('/ticket/validate', headers=headers, data=json.dumps(validate_data), content_type='application/json')
        #print(validate_response.data)
        time1 = time.time() # end time

        response_times.append((time1 - time0) * 1000) # in milliseconds
    
    
    # average
    avg_response_time = np.mean(response_times)
    
    # plot the results as a line graph
    x = range(1, 1001) # number of response time measurements
    y = response_times
    plt.plot(x, y)
    
    # plot the average as a red line and annotate its value
    plt.axhline(y=avg_response_time, color='r', linestyle='--')
    plt.annotate(f'Average: {avg_response_time:.2f} ms', xy=(0.5, avg_response_time), xytext=(5, -10),
             textcoords='offset points', ha='center', color='r')

    plt.xlabel('Run')
    plt.ylabel('Response time (ms)')
    plt.show()

if __name__ == "__main__":
    with app.app_context():
        reponse_time()