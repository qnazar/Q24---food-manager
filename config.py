import os
from dotenv import load_dotenv


load_dotenv()


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
    DEBUG = True
    PG_USER = os.environ.get('PG_USER')
    PG_PSSWRD = os.environ.get('PG_PSSWRD')
    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get('PG_PORT')
    PG_DATABASE = os.environ.get('PG_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@localhost/{PG_DATABASE}"
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
