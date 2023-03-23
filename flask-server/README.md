# Flask
## Introduction
This README gives the instructions on how to setup and run the Flask server bare metal.
## Requirements
To run this application, you will need:
* Python 3.10+

To install the required Python libraries, run the command:
```cmd
pip install -r requirements.txt
```
## Environment File
### Basic Setup
To run the Flask server bare metal, create a `.env` file in the `flask-server` directory with the following contents:
```.env
SECRET_KEY=<YOUR_SECURE_SECRET_KEY>
JWT_SECRET_KEY=<YOUR_SECURE_JWT_KEY>
SELF_SIGNED=True
HOST=<YOUR_IP_ADDRESS>
```
### MySQL
By default, Flask will default to using a SQLite Database.

To use a MySQL server running on the same host, add the following to your `.env` file:
```.env
MYSQL_HOST=localhost
MYSQL_DATABASE=<DATABASE_NAME>
MYSQL_USER=<USER_NAME>
MYSQL_PASSWORD=<PASSWORD>
```
### Developer Mode
To run Flask in developer mode, add the following to your `.env` file:
```.env
DEV_MODE=True
```
## Running Flask
### Start Up
To start up the Flask server, run the following command in terminal:
```cmd
python app.py
```
### Documentation
To access the documentation and see the routes for the application, in your web browser navigate to:
```
https://<YOUR_IP_ADDRESS>:5000/docs
```
## Sample Data
To populate the database with some sample data, run the command:
```cmd
python sample_data.py
```
This command will create the following users that can be used in the application:
* **Test user:**
  * Email: `test@test.com`
  * Password: `test1234`
* **Management user:**
  * Email: `admin@test.com`
  * Password: `test1234`

