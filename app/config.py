"""Flask configuration."""
from os import path


basedir = path.abspath(path.dirname(__file__))


class Config:
    """Base config."""
    STATIC_FOLDER = 'Templates'
    FLASK_APP = 'main.py'
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@db/webavance_db'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/webavance'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@db/webavance_db'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/webavance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
