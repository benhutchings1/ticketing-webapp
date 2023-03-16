import json
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import create_app, db
from models import User
import time
import matplotlib.pyplot as plt
import numpy as np

app = create_app('config.TestConfig')

client = app.test_client()

def setUp():
    with app.app_context():
        db.create_all()
        test_user = User(
            email_address='test@test.com',
            passwd_hash=generate_password_hash('test', method="sha256", salt_length=32),
            firstname='Test',
            surname='Test',
            date_of_birth=datetime.strptime('2000-01-01', "%Y-%m-%d").date(),
            postcode='AB12 3DC',
            phone_number=f'07345345',
            role='user'
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
        "password": "test",
        "firstname": "test",
        "surname": "test",
        "date_of_birth": "2023-03-16",
        "postcode": "test1234",
        "phone_number": "345345"
    }
    login_data = {
            "email_address": "test@test.com",
            "password": "test"
        }
    signup_response = client.post('/signup', data=json.dumps(data), content_type='application/json')
    login_response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    return login_response

def reponse_time():
    ''' This method measures the reponse time of an endpoint in milliseconds
        Here, it is being used with /account route
        but it is meant to measure the reponse time of
        /addticket
        /requestQRdata
        /validateTicket
    '''
    
    access_token = singup_and_login().json['token']
    headers = {'Authorization': f'Bearer {access_token}'}

    response_times = []
    for i in range(1000):
        
        time0 = time.time() # start time
        #print(client.get('/account', headers=headers).data) # remove print() from accurate time measurement
        client.get('/account', headers=headers).data
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
        setUp()
        singup_and_login()
        reponse_time()