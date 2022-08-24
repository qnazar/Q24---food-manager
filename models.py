from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


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

    BMI = db.Column(db.Float())  # індекс маси тіла
    BMR = db.Column(db.Integer)  # основний обмін
    DKI = db.Column(db.Integer)  # денна норма ккал
    DWN = db.Column(db.Integer)  # денна норма води
    IW = db.Column(db.Float())   # ідеальна вага
    min_weight = db.Column(db.Float())
    max_weight = db.Column(db.Float())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='profile')
    dynamics = db.relationship('ProfileDynamic', backref='profile', lazy=True)

    def body_mass_index(self):
        BMI = self.weight / (self.height / 100) ** 2
        return round(BMI, 2)

    def basic_metabolism_rate(self):
        """Формула Міффліна - Сан Жеора"""
        age = (datetime.date.today() - self.birthday).total_seconds() // (60 * 60 * 24 * 365)
        k = 5 if self.sex == 'Чоловіча' else -161
        BMR = 9.99 * self.weight + 6.25 * self.height - 4.92 * age + k
        return round(BMR)

    def daily_kcal_intake(self):
        BMR = self.basic_metabolism_rate()
        SDFE = BMR / 10  # специфічно-динамічна дія їжі
        return round((BMR + SDFE) * self.activity)

    def water_norm(self):
        hnw = self.max_normal_weight()
        overweight = self.weight - hnw if self.weight > hnw else 0
        return round(35 * self.weight + overweight * 20)

    def ideal_weight(self):
        iw = (self.height - 100) - (self.height - 150) / 4
        if self.constitution == 'Астенік':
            iw = iw - iw/10
        elif self.constitution == 'Гіперстенік':
            iw = iw + iw/10
        return round(iw, 1)

    def max_normal_weight(self):
        """Розрахунок Кетле"""
        return round(25 * (self.height/100)**2, 1)

    def min_normal_weight(self):
        """Розрахунок Кетле"""
        return round(18.5 * (self.height/100)**2, 1)

    def __str__(self):
        return f'<Profile: {self.first_name} {self.last_name}>'


class ProfileDynamic(db.Model):
    __tablename__ = 'profile_dynamic'

    id = db.Column(db.Integer, primary_key=True)
    current_weight = db.Column(db.Float())
    current_activity = db.Column(db.Float())
    BMR = db.Column(db.Integer)
    BMI = db.Column(db.Float())
    DKI = db.Column(db.Integer)
    DWN = db.Column(db.Integer)
    entry_date = db.Column(db.Date, default=datetime.date.today())

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))


class ProductsCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

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
    shop_list = db.relationship('ShoppingList', backref='product', lazy=True)
    ingredient = db.relationship('Ingredient', backref='product', lazy=True)

    category_id = db.Column(db.Integer(), db.ForeignKey('product_category.id'))

    def __repr__(self):
        return f'<Product: {self.name}>'

    def __str__(self):
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

    def __str__(self):
        return f'<Stock: {self.id}>'


class Trash(db.Model):
    __tablename__ = 'trash'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))
    price = db.Column(db.Float())
    date_thrown = db.Column(db.Date, default=datetime.date.today())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __str__(self):
        return f'<Trash: {self.product.name}'


class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))
    bought = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __str__(self):
        return f'<Shoplist: {self.product_name}'


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    time = db.Column(db.Integer)
    complexity = db.Column(db.String(32))
    description = db.Column(db.Text)
    instruction = db.Column(db.Text)
    picture = db.Column(db.String)

    ingredient = db.relationship('Ingredient', backref='recipe', lazy=True)

    def __str__(self):
        return self.name


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    type = db.Column(db.String)
    weight = db.Column(db.Float)
    kcal = db.Column(db.Integer)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fibers = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.datetime.now())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
