# API configuration
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)


class DevConfig(Config):
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
