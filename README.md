# Ticketing Web Application
Group 4 web app

## Getting started
### Setting up the environment file for Flask
Create a file with the filename `.env` in the `flask-server` directory with the following contents:
```.env
SECRET_KEY='<YOUR_SECURE_SECRET_KEY>'
JWT_SECRET_KEY='<YOUR_SECURE_JWT_KEY>'
```
If you wish to run Flask in developer mode, add the following to your `.env` file:
```.env
DEV_MODE=True
```