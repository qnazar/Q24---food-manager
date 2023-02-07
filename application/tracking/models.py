import datetime

from application import db


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
