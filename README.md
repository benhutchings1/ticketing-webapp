# Ticketing Web Application
Group 4 web app

## Getting started
### Setting up the environment file for Flask
Create a file with the filename `.env` in the `flask-server` directory with the following contents:
```.env
SECRET_KEY='<YOUR_SECURE_SECRET_KEY>'
JWT_SECRET_KEY='<YOUR_SECURE_JWT_KEY>'
SELF_SIGNED=True
```
If you wish to run Flask in developer mode, add the following to your `.env` file:
```.env
DEV_MODE=True
```
If you wish to use MySQL, add the following to your `.env` file:
```.env
MYSQL=True
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=<DATABASE_NAME>
MYSQL_USER=<DATABASE_USERNAME>
MYSQL_PASSWORD=<DATABASE_PASSWORD>
```
### Setting up the environment file for MySQL and Docker
To MySQL with Docker, create a file with the filename `.env` in the root directory containing `docker-compose.yml` with the following contents:
```.env
MYSQL_DATABASE=<DATABASE_NAME>
MYSQL_USER=<DATABASE_USERNAME>
MYSQL_PASSWORD=<DATABASE_PASSWORD>
```