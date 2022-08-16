from flask_sqlalchemy import SQLAlchemy, BaseQuery
import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class CustomQuery(BaseQuery):
    def get_or_None(self, ident):
        return self.get(ident) or None


db = SQLAlchemy(query_class=CustomQuery)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.now())
    email = db.Column(db.String(80), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String)

    profile = relationship('Profile', uselist=False, back_populates='user')
    stocks = relationship('Stock', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not visible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def person(self):
        return Profile.query.get(self.id)

    # @property
    # def stock(self):
    #     return Stock.query(Stock).filter(Stock.user_id == self.id)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    sex = db.Column(db.String(10))
    birthday = db.Column(db.Date)

    weight = db.Column(db.Float())
    height = db.Column(db.Integer)
    constitution = db.Column(db.String(32))
    activity = db.Column(db.Float())

    # BMI = db.Column(db.Float(precision=2))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='profile')

    def body_mass_index(self):
        BMI = self.weight / (self.height / 100) ** 2
        return round(BMI, 2)

    def basic_metabolism_rate(self):
        """Формула Міффліна - Сан Жеора"""
        age = (datetime.date.today() - self.birthday).total_seconds() // (60 * 60 * 24 * 365)
        if self.sex == 'Male':
            BMR = 9.99 * self.weight + 6.25 * self.height - 4.92 * age + 5
            # BMR = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * age)
        elif self.sex == 'Female':
            BMR = 9.99 * self.weight + 6.25 * self.height - 4.92 * age - 161
            # BMR = 447.6 + (9.2 * self.weight) + (3.1 + self.height) - (4.3 * age)
        else:
            raise ValueError
        return int(BMR)

    def daily_kcal_intake(self):
        BMR = self.basic_metabolism_rate()
        SDFE = BMR / 10  # специфічно-динамічна дія їжі
        return round((BMR + SDFE) * self.activity)

    def highest_normal_weight(self):
        return round(25 * (self.height/100)**2, 1)

    def water_norm(self):
        hnw = self.highest_normal_weight()
        overweight = self.weight - hnw if self.weight > hnw else 0
        return round(35 * self.weight + overweight * 20)

    def ideal_weight(self):
        iw = (self.height - 100) - (self.height - 150) / 4
        if self.constitution == 'Astenic':
            iw = iw - iw/10
        elif self.constitution == 'Hyperstenic':
            iw = iw + iw/10
        return round(iw, 1)


class ProductsCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    kcal = db.Column(db.Integer())
    proteins = db.Column(db.Float())
    fats = db.Column(db.Float())
    carbs = db.Column(db.Float())
    fibers = db.Column(db.Float())
    stocks = db.relationship('Stock', backref='product', lazy=True)
    trash = db.relationship('Trash', backref='product', lazy=True)

    category_id = db.Column(db.Integer(), db.ForeignKey('product_category.id'))

    def __repr__(self):
        return self.name


class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))  # г кг шт л мл
    produced_date = db.Column(db.Date)
    expired_date = db.Column(db.Date)
    price = db.Column(db.Float())
    date_added = db.Column(db.Date, default=datetime.date.today())
    status = db.Column(db.String(64), default='нове')  # new in-use fully-used expired thrown-away

    @property
    def produced(self):
        return self.produced_date.strftime('%d-%m-%Y')

    @property
    def expired(self):
        return self.expired_date.strftime('%d-%m-%Y')


class Trash(db.Model):
    __tablename__ = 'trash'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))
    price = db.Column(db.Float())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # def __repr__(self):
    #     return self.product_name
