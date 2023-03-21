# API configuration
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

if config('MYSQL', cast=bool, default=False):
    DATABASE = f"mysql://{config('MYSQL_USER')}:{config('MYSQL_PASSWORD')}@" \
               f"{config('MYSQL_HOST')}:{config('MYSQL_PORT')}/{config('MYSQL_DATABASE')}"
else:
    DATABASE = "sqlite:///" + os.path.join(BASE_DIR, 'dev.db')


class Config:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    SQLALCHEMY_DATABASE_URI = DATABASE
    SELF_SIGNED = config('SELF_SIGNED', cast=bool, default=False)


class DevConfig(Config):
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = True
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    DEBUG = True


class TestConfig:
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_CSRF_IN_COOKIES = False
    WTF_CSRF_ENABLED = False
    JWT_CSRF_METHODS = []
    JWT_TOKEN_LOCATION = "cookies"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = True


current_config = DevConfig if config('DEV_MODE', cast=bool, default=False) else Config
