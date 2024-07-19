import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345qwerty'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
