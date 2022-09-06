import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, session
from flask_login import login_required, current_user

from application import db
from models import Product, Stock, Trash, ShoppingList, Meal
from forms import StockForm, ShoppingForm, TrashFilterForm, UseProductForm, ProductsForMealForm, AddMealForm
from helpers import sort_the_stock, use_from_stock, stock_statistics, measure_converter


tracking_bp = Blueprint('tracking_bp', __name__, template_folder='templates',
                        static_folder='static', static_url_path='/tracking/static')


@tracking_bp.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    all_products = Product.query.all()  # всі продукти з бази - для пошуку
    products = sort_the_stock(current_user)  # відсортовані продукти юзера
    trash = Trash.query.filter_by(user_id=current_user.id).all()  # викинуті юзером продукти
    trash_sum = sum([p.price for p in trash]) if trash else 0

    form = StockForm()
    use_product_form = UseProductForm()

    if form.validate_on_submit() and form.add.data:
        try:
            product_id = Product.query.filter_by(name=form.name.data).first().id
            entry = Stock(user_id=current_user.id, product_id=product_id,
                          quantity=form.quantity.data, measure=form.measure.data,
                          produced_date=form.produced_date.data, expired_date=form.expired_date.data,
                          price=form.price.data)
            db.session.add(entry)
            db.session.commit()
            products = sort_the_stock(current_user)
            flash('Продукт додано', category='success')
        except Exception as e:
            flash('Наразі можна додати тільки продукти, які є в нашій базі.')
            print(e)
    if use_product_form.validate_on_submit() and use_product_form.submit.data:
        used: Stock = Stock.query.get(use_product_form.stock.data)
        quantity = use_product_form.quantity.data
        success = use_from_stock(used, quantity)
        flash('Продукт використано') if success else flash('Нема стільки продукту')
    return render_template('stock.html', form=form, products=products, title='Мої продукти',
                           all_products=all_products, trash=trash_sum, use_product_form=use_product_form)


@tracking_bp.route('/full_use/<int:id>')
def full_use(id):
    entry: Stock = Stock.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Продукт повністю використано!')
    return redirect(url_for('tracking_bp.stock'))


@tracking_bp.route('/throw_away/<int:id>')
def throw_away(id):
    entry: Stock = Stock.query.get(id)
    trash: Trash = Trash(product_id=entry.product_id, quantity=entry.quantity,
                         measure=entry.measure, price=entry.price, user_id=current_user.id)
    db.session.add(trash)
    db.session.delete(entry)
    db.session.commit()
    flash("Продукт викинуто")
    return redirect(url_for('tracking_bp.stock'))


@tracking_bp.route('/product/<int:id>')
def product_info(id):
    product = Product.query.get_or_404(id)
    return render_template('product_info.html', product=product)


@tracking_bp.route('/shopping_list', methods=['GET', 'POST'])
def shopping_list():
    all_products = Product.query.all()
    shop_list = ShoppingList.query.filter_by(user_id=current_user.id).all()
    form = ShoppingForm()
    modal_form = StockForm()
    if form.validate_on_submit() and form.submit.data:
        product_id = Product.query.filter_by(name=form.name.data).first().id
        shop_item = ShoppingList(product_id=product_id, user_id=current_user.id,
                                 quantity=form.quantity.data, measure=form.measure.data)
        db.session.add(shop_item)
        db.session.commit()
        flash('Новий продукт у списку покупок')
        shop_list = ShoppingList.query.filter_by(user_id=current_user.id).all()
        return render_template('shopping_list.html', form=form, all_products=all_products,
                               shop_list=shop_list, modal_form=modal_form)
    if modal_form.validate_on_submit() and modal_form.add.data:
        product_id = Product.query.filter_by(name=modal_form.name.data).first().id
        entry = Stock(user_id=current_user.id, product_id=product_id,
                      quantity=modal_form.quantity.data, measure=modal_form.measure.data,
                      produced_date=modal_form.produced_date.data, expired_date=modal_form.expired_date.data,
                      price=modal_form.price.data)
        shop_item = ShoppingList.query.filter_by(user_id=current_user.id, product_id=entry.product_id).first()
        db.session.add(entry)
        db.session.delete(shop_item)
        db.session.commit()
        flash("Продукт куплено та додано у ваші продукти!")
        shop_list = ShoppingList.query.filter_by(user_id=current_user.id).all()
        return render_template('shopping_list.html', form=form, all_products=all_products,
                               shop_list=shop_list, modal_form=modal_form)
    return render_template('shopping_list.html', form=form, all_products=all_products,
                           shop_list=shop_list, modal_form=modal_form)


@tracking_bp.route('/shopping_list/remove/<int:id>')
@login_required
def remove_from_shopping_list(id):
    item = ShoppingList.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Продукт видалено зі списку!')
    return redirect(url_for('tracking_bp.shopping_list'))


@tracking_bp.route('/trash', methods=['GET', 'POST'])
@login_required
def trash_page():
    form = TrashFilterForm()
    trash = Trash.query.filter(Trash.user_id == current_user.id, Trash.date_thrown >= datetime.date.today()).all()
    options = {'day': datetime.date.today(),
               'week': datetime.date.today() - datetime.timedelta(days=7),
               'month': datetime.date.today() - datetime.timedelta(days=30),
               'year': datetime.date.today() - datetime.timedelta(days=365)}
    stats = stock_statistics(trash)
    if form.validate_on_submit():
        trash = Trash.query.filter(Trash.user_id == current_user.id,
                                   Trash.date_thrown >= options[form.choice.data]).all()
        stats = stock_statistics(trash)
    return render_template('trash.html', title='Смітник', trash=trash, form=form, stats=stats)



@tracking_bp.route('/meal', methods=['GET', 'POST'])
@login_required
def meal():
    all_products = Stock.query.filter_by(user_id=current_user.id).all()
    product_form = ProductsForMealForm()
    meal_form = AddMealForm()

    if 'products' not in session or 'results' not in session:
        session['products'] = {}
        session['results'] = {'weight': 0, 'kcal': 0, 'proteins': 0, 'fats': 0, 'carbs': 0, 'fibers': 0}

    if product_form.validate_on_submit() and product_form.add.data:

        product = Product.query.filter_by(name=product_form.product.data).first()
        if not product:
            flash('Невідомий продукт')
        elif s := Stock.query.filter_by(product_id=product.id, user_id=current_user.id).first():
            if s.measure != product_form.measure.data:
                flash(f'Продукт має бути вказаний в "{s.measure}"')
            elif s.product.name in session['products']:
                flash('Цей продукт вже додано')
            elif product_form.quantity.data > s.quantity:
                flash('Нема стільки продукту')
            else:
                session['products'][str(product)] = {'weight': (product_form.quantity.data, product_form.measure.data)}
                weight = round(measure_converter(product_form.quantity.data, product_form.measure.data), 2)
                session['results']['weight'] += weight
                for key, value in session['results'].items():
                    if key == 'weight':
                        continue
                    session['results'][key] += round((getattr(product, key) * weight) / 100, 1)
                    session['products'][str(product)].update([(key, round(getattr(product, key) * weight / 100, 1))])

    if meal_form.validate_on_submit() and meal_form.clear.data:
        session['products'] = {}
        session['results'] = {'weight': 0, 'kcal': 0, 'proteins': 0, 'fats': 0, 'carbs': 0, 'fibers': 0}

    if meal_form.validate_on_submit() and meal_form.submit.data:
        if session['products'] == {}:
            flash('Потрібно додати продукти в страву')
            return redirect(url_for('tracking_bp.meal'))
        new_meal = Meal(name=meal_form.name.data, type=meal_form.meal.data, user_id=current_user.id,
                        weight=round(session['results']['weight'], 2), kcal=session['results']['kcal'],
                        protein=round(session['results']['proteins'], 1), fat=round(session['results']['fats'], 1),
                        carbs=round(session['results']['carbs'], 1), fibers=round(session['results']['fibers'], 1))

        for product_name, values in session['products'].items():
            product = Product.query.filter_by(name=product_name).first()
            s: Stock = Stock.query.filter_by(product_id=product.id, user_id=current_user.id).first()
            price_per_unit = round(s.price / s.quantity, 2)
            s.quantity -= float(values['weight'][0])
            s.quantity = round(s.quantity, 2)
            s.status = 'у вжитку' if s.quantity > 0 else 'використано'
            s.price = round(s.quantity * price_per_unit, 2)

        db.session.add(new_meal)
        db.session.commit()
        flash("Страву додано")

        session['products'] = {}
        session['results'] = {'weight': 0, 'kcal': 0, 'proteins': 0, 'fats': 0, 'carbs': 0, 'fibers': 0}

    return render_template('meal.html', products_form=product_form, results=session['results'],
                           meal_form=meal_form, products=session['products'], all_products=all_products)


@login_required
@tracking_bp.route('/meal_nutrition_calculator', methods=['GET', 'POST'])
def meal_nutrition_calculator():
    """Калькулятор калорійності страв. Доступний без логіну, нічого не зберігає"""
    all_products = Product.query.all()
    product_form = ProductsForMealForm()
    meal_form = AddMealForm()

    if 'products2' not in session or 'results2' not in session:
        session['products2'] = {}
        session['results2'] = {'weight': 0, 'kcal': 0, 'proteins': 0, 'fats': 0, 'carbs': 0, 'fibers': 0}

    if product_form.validate_on_submit() and product_form.add.data:

        product = Product.query.filter_by(name=product_form.product.data).first()
        if not product:
            flash("В базі немає такого продукту")
        elif product.name in session['products2']:
            flash("Цей продукт вже додано")
        else:
            session['products2'][str(product)] = {'weight': (product_form.quantity.data, product_form.measure.data)}
            weight = round(measure_converter(product_form.quantity.data, product_form.measure.data), 2)
            session['results2']['weight'] += weight
            for key, value in session['results2'].items():
                if key == 'weight':
                    continue
                session['results2'][key] += round(getattr(product, key) * weight / 100, 1)
                session['products2'][str(product)].update([(key, round(getattr(product, key) * weight / 100, 1))])

    if meal_form.validate_on_submit() and meal_form.clear.data:
        session['products2'] = {}
        session['results2'] = {'weight': 0, 'kcal': 0, 'proteins': 0, 'fats': 0, 'carbs': 0, 'fibers': 0}

    return render_template('meal_nutrition_calculator.html', title='Калорійність', all_products=all_products,
                           products=session['products2'], product_form=product_form, meal_form=meal_form,
                           results=session['results2'])

