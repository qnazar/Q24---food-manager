import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=r'C:\Users\user\Documents\GitHub\food\env\local\.env')


class BaseConfig:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    FOLDER_TO_UPLOAD = 'static/images/profiles/'
    FOLDER_TO_UPLOAD_RECIPES = 'static/images/recipes/'
    SECRET_KEY = os.environ.get('SECRET_KEY')

    PG_USER = os.environ.get('PG_USER')
    PG_PSSWRD = os.environ.get('PG_PSSWRD')
    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get('PG_PORT')
    PG_DATABASE = os.environ.get('PG_DATABASE')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
