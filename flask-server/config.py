# API configuration
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    JWT_TOKEN_LOCATION = "cookies"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://group4:TruckForumUpset1!@92.239.221.181 :3306/ticketing_app" #"sqlite:///" + os.path.join(BASE_DIR, 'main.db')


class DevConfig(Config):
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    JWT_TOKEN_LOCATION = "cookies"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://group4:TruckForumUpset1!@92.239.221.181 :3306/ticketing_app" #"sqlite:///" + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True


current_config = DevConfig if config('DEV_MODE', cast=bool, default=False) else Config
