import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from itsdangerous import URLSafeTimedSerializer

from config import DevelopmentConfig as Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
mail = Mail()


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    mail.init_app(app)

    with app.app_context():
        db.create_all()

        from .home import routes as home
        from .auth import routes as auth
        from .profile import routes as profile
        from .recipes import routes as recipes
        from .tracking import routes as track

        app.register_blueprint(home.home_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(profile.profile_bp)
        app.register_blueprint(recipes.recipes_bp)
        app.register_blueprint(track.tracking_bp)

        return app
