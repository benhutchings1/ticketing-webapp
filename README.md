<img src="frontend/src/img/logo-01.png" width="150" alt="Secure Tickets Logo"/>

# Secure Tickets (Ticketing Web Application)
## Introduction
Secure Tickets, created as part of a Stage 4/Masters team project, is a web application for a secure ticketing system for in-person events. This application allows users to buy tickets for events and present their ticket as a QR Code. Management users, within this system, are able to scan tickets and verify their authenticity. The main security of this application employs a digital signature scheme to maintain ticket integrity of the QR code and encryption to maintain ticket confidentiality through a secure connection.


This application uses the following web stack:
* Flask
* React
* MySQL
* Nginx
## Getting started with Docker
### Requirements
You will need to install:
* Docker

**Note:** If you do not wish to run the application with Docker, go to the [Running the Application Bare Metal](#Running-the-Application-Bare-Metal) section.
### Creating the Environment File
In the root folder containing `docker-compose.yml`, create the file `.env` with the following contents:
```.env
# Flask
SECRET_KEY=<YOUR_SECURE_SECRET_KEY>
JWT_SECRET_KEY=<YOUR_SECURE_JWT_KEY>

# MySQL
MYSQL_DATABASE=<DATABASE_NAME>
MYSQL_USER=<USER_NAME>
MYSQL_PASSWORD=<PASSWORD>

# Host Address
HOST=<YOUR_IP_ADDRESS>
```
### Running Docker
To start up the application, run the command:
```cmd
docker-compose up
```
**Note:** It may take a long time to build for the first time.

To stop the application, run the command:
```cmd
docker-compose stop
```
### Populating the Database
To populate the database with some sample data, run the command:
```cmd
docker exec ticketing-webapp-flask-1 python sample_data.py
```
This command will create the following users that can be used in the application:
* **Test user:**
  * Email: `test@test.com`
  * Password: `test1234`
* **Management user:**
  * Email: `admin@test.com`
  * Password: `test1234`

Events are also created and have a start time based on when the sample data script is ran. 
### Accessing the Application
In your web browser, navigate to:
```
https://<YOUR_IP_ADDRESS>
```
## Running the Application Bare Metal
To run this application bare metal, you will need to run Flask and React separately.

For more details, read the individual README files:
* [Flask](flask-server/README.md)
* [React](frontend/README.md)

## Screenshots
