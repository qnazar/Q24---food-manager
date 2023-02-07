import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_celeryext import FlaskCeleryExt
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from itsdangerous import URLSafeTimedSerializer

from application.config import config
from application.celery_utils import make_celery


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
mail = Mail()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    mail.init_app(app)
    ext_celery.init_app(app)

    # register blueprints
    from application.auth import auth_bp
    from application.home import home_bp
    from application.profile import profile_bp
    from application.recipes import recipes_bp
    from application.tracking import tracking_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(tracking_bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
