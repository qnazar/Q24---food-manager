from models import db, Stock, ProductsCategory
import datetime


def stock_statistics(stocks: list) -> dict:
    result: dict = {'count': 0, 'weight': 0, 'price': 0, 'kcal': 0,
                    'protein': 0, 'fat': 0, 'carb': 0, 'fiber': 0}
    for item in stocks:
        measure = 1 if item.measure in {'г', 'мл'} else 1000
        if item.measure == 'шт':  # для прикладу. Тільки для яєць
            measure = 60  # Середня вага одного яйця - 60 г
        product = item.product
        result['count'] += 1
        result['weight'] += round(item.quantity * measure, 1)
        result['price'] += round(item.price, 2)
        result['kcal'] += round(product.kcal * item.quantity * measure // 100)
        result['protein'] += round(product.proteins * item.quantity * measure // 100, 1)
        result['fat'] += round(product.fats * item.quantity * measure // 100, 1)
        result['carb'] += round(product.carbs * item.quantity * measure // 100, 1)
        result['fiber'] += round(product.fibers * item.quantity * measure // 100, 1)
    return result


def sort_the_stock(current_user, cat_id=0):  # not working category filtering
    if cat_id == 0:
        users_stock = Stock.query.filter_by(user_id=current_user.id).order_by(Stock.expired_date).all()
    else:
        users_stock = Stock.query.filter(Stock.user_id == current_user.id,
                                         Stock.product.category_id == cat_id).order_by(Stock.expired_date).all()
    if not users_stock:
        return []
    output = []
    for item in users_stock:
        date = item.expired_date - datetime.date.today()
        if date.days < 0:
            item.status = ':('
            db.session.commit()
            output.append(('', [item]))
        else:
            output.append((f'{date.days} дн', [item]))
    return output


def select_query():
    """Helper function to generate SelectField choices"""
    choices = []
    query = ProductsCategory.query.all()
    for q in query:
        choices.append((q.id, q.name))
    return choices


def measure_converter(quantity, unit):
    """Helper for converting measure to GRAMS"""
    if unit in {'г', 'мл'}:
        return quantity
    elif unit in {'кг', 'л'}:
        return quantity * 1000
    elif unit == 'шт':  # Конвертація відбувається на основі середньої ваги яєць. Потрібна таблиця конвертації в базі
        return quantity * 60


def use_from_stock(item: Stock, quantity: int) -> bool:
    if quantity <= item.quantity:
        price_per_unit = item.price / item.quantity
        item.quantity -= float(quantity)
        item.quantity = round(item.quantity, 3)
        item.status = 'у вжитку' if item.quantity > 0 else 'використано'
        item.price = round(item.quantity * price_per_unit, 2)
        db.session.commit()
        return True
    return False
