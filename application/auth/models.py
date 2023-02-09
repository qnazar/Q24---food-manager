import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from application import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.now())
    email = db.Column(db.String(80), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String)

    profile = relationship('Profile', uselist=False, back_populates='user')
    stock = relationship('Stock', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not visible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
