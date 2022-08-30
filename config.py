import os


class Config(object):
    DEBUG = False
    TESTING = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    FOLDER_TO_UPLOAD = 'static/images/profiles/'
    FOLDER_TO_UPLOAD_RECIPES = 'static/images/recipes/'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    PG_USER = os.environ.get('PG_USER')
    PG_PSSWRD = os.environ.get('PG_PSSWRD')
    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get('PG_PORT')
    PG_DATABASE = os.environ.get('PG_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@localhost/{PG_DATABASE}"


class ProductionConfig(Config):
    DATABASE_URL = os.environ.get('DATABASE_URL')


# TODO need to fix deploy db connection
#DATABASE_URL = 'postgresql://mndnusjyggiwvj:fe99a1c7b460e709520e0b6d1796590849362ac37af68923a2815e9c36cbaa7c@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d2tsirtb3pcjm3'


# SQLALCHEMY_DATABASE_URI = DATABASE_URL

