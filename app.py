import datetime

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_migrate import Migrate
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import uuid
import os

from models import db, User, Profile, Stock, Product, ProductsCategory, Trash
from forms import RegisterForm, LoginForm, ProfileForm, ProfilePicForm, CalcForm, StockForm, ProductForm, UseProductForm

app = Flask(__name__)
app.config.from_pyfile('config.py')

# DB initialization
db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

csrf = CSRFProtect()
csrf.init_app(app)

# Mail agent for email confirmation and serializer
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():

        # checking for user with unique email
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:  # no such email was used
            user = User(email=form.email.data, password_hash=generate_password_hash(form.password.data))
            # adding user to the db
            db.session.add(user)
            db.session.commit()
            login_user(user)  # autologin after registration
            flash('Реєстраці пройшла успішно. Лист з підтвердженням відправлено на вашу електронну адресу',
                  category='success')

            # sending email confirmation
            token = s.dumps(user.email, salt='email-confirm')
            msg = Message('Confirm email', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = f'Your link is {link}'
            mail.send(msg)

            return redirect(location=url_for('user', id=user.id))
        else:
            flash('This email is already used', category='warning')
    return render_template('registration.html', title='Registration', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=900)
        flash('Email confirmed!!!', category='success')
        current_user.email_confirmed = True
        db.session.commit()
    except SignatureExpired:
        return 'Signature time expired'
    return redirect(url_for('user', id=current_user.id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login successfully', category='success')
                return redirect(url_for('user', id=user.id))
            else:
                flash('Неправильний пароль', category='danger')
        else:
            flash('Немає користувача з такою електронною адресою', category='danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('До зустрічі!', category='success')
    return redirect(url_for('login'))


def stock_statistics(stocks: list) -> dict:
    result: dict = {'count': 0, 'weight': 0, 'price': 0, 'kcal': 0,
                    'protein': 0, 'fat': 0, 'carb': 0, 'fiber': 0}
    for stock in stocks:
        measure = 1 if stock.measure in {'г', 'мл'} else 1000
        if stock.measure == 'шт':  # для прикладу. Тільки для яєць
            measure = 60  # Середня вага одного яйця - 60 г
        product = stock.product
        result['count'] += 1
        result['weight'] += round(stock.quantity * measure, 1)
        result['price'] += round(stock.price, 2)
        result['kcal'] += round(product.kcal * stock.quantity * measure // 100)
        result['protein'] += round(product.proteins * stock.quantity * measure // 100, 1)
        result['fat'] += round(product.fats * stock.quantity * measure // 100, 1)
        result['carb'] += round(product.carbs * stock.quantity * measure // 100, 1)
        result['fiber'] += round(product.fibers * stock.quantity * measure // 100, 1)
    return result


@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    if id != current_user.id:
        abort(403)
    profile = Profile.query.get(id)
    if not profile:
        profile = Profile(id=current_user.id, user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    stats = stock_statistics(stocks)
    trashes = Trash.query.filter_by(user_id=current_user.id).all()
    trash = stock_statistics(trashes)
    return render_template('user.html', title='Profile', user=current_user, person=profile, stats=stats, trash=trash)


@app.route('/user/<int:id>/update', methods=['GET', 'POST'])
def update_personal_info(id):
    if id != current_user.id:
        abort(403)
    person = current_user.profile
    form = ProfileForm(sex=person.sex, constitution=person.constitution)
    if form.validate_on_submit():
        if form.first_name.data:
            person.first_name = form.first_name.data
        if form.last_name.data:
            person.last_name = form.last_name.data
        if form.sex.validate_choice:
            person.sex = form.sex.data
        if form.birthday.data:
            person.birthday = form.birthday.data
        if form.weight.data:
            person.weight = form.weight.data
        if form.height.data:
            person.height = form.height.data
        if form.constitution.data:
            person.constitution = form.constitution.data
        if form.activity.data:
            person.activity = form.activity.data
        db.session.commit()
        flash('Інфо оновлено!', category='success')
        return redirect(url_for('user', id=current_user.id))
    return render_template('update.html', title='Update Info', user=current_user, form=form, person=person)


@app.route('/upload_picture', methods=['GET', 'POST'])
@login_required
def upload_picture():
    form = ProfilePicForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            if current_user.profile_pic:
                os.remove(os.path.join(f'static/images/profiles/{current_user.profile_pic}'))

            picture = request.files['profile_pic']
            pic_filename = secure_filename(picture.filename)
            pic_name = str(uuid.uuid1()) + '_' + pic_filename

            picture.save(os.path.join(app.config['FOLDER_TO_UPLOAD'], pic_name))
            current_user.profile_pic = pic_name
            db.session.commit()
            flash(message='Фото успішно оновлено', category='success')
        return redirect(url_for('user', id=current_user.id))
    return render_template('upload_picture.html', title='Upload profile pic', form=form)


@app.route('/delete_picture')
@login_required
def delete_picture():
    if current_user.profile_pic is None:
        pass
    else:
        print("work")
        os.remove(os.path.join(f'static/images/profiles/{current_user.profile_pic}'))
        current_user.profile_pic = None
        db.session.commit()
        flash(message='Фото успішно видалено', category='success')
    return redirect(url_for('user', id=current_user.id))


@app.route('/calculations/<mode>', methods=['GET', 'POST'])
@login_required
def calculations(mode):
    if mode == 'about':
        return render_template('calculations.html')
    form = CalcForm(weight=current_user.profile.weight)
    if form.validate_on_submit():
        current_user.profile.weight = form.weight.data
        db.session.commit()
        if mode == 'water':
            water = current_user.profile.water_norm()
            current_user.profile.DWN = water
            flash(f'Твоя денна норма води - {water} мл!')
        elif mode == 'kcal':
            kcal = current_user.profile.daily_kcal_intake()
            current_user.profile.DKI = kcal
            flash(f'Твоя денна норма калорій - {kcal} ккал!')
        elif mode == 'imt':
            imt = current_user.profile.body_mass_index()
            current_user.profile.BMI = imt
            flash(f'Твій індекс маси тіла - {imt}!')
        elif mode == 'weight':
            weight = current_user.profile.ideal_weight()
            current_user.profile.IW = weight
            flash(f'Твоя ідеальна вага - {weight} кг!')
        db.session.commit()
        return redirect(url_for('user', id=current_user.id))
    return render_template('calculations.html', form=form)


def sort_the_stock(current_user):
    stock: Stock = Stock.query.filter_by(user_id=current_user.id).order_by(Stock.expired_date).all()
    if not stock:
        return []
    output = []
    for s in stock:
        date = s.expired_date - datetime.date.today()
        if date.days < 0:
            s.status = ':('
            db.session.commit()
            output.append(('', [s]))
        else:
            output.append((f'{date.days} дн', [s]))
    return output


@app.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    all_products = Product.query.all()  # всі продукти з бази - для пошуку
    products = sort_the_stock(current_user)  # відсортовані продукти юзера
    trash = Trash.query.filter_by(user_id=current_user.id).all()  # викинуті юзером продукти
    trash_sum = sum([p.price for p in trash]) if trash else 0

    form = StockForm()
    use_product_form = UseProductForm()

    if form.validate_on_submit():
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
        return render_template('stock.html', form=form, products=products, title='Мої продукти',
                               all_products=all_products, trash=trash_sum, use_product_form=use_product_form)
    if use_product_form.validate_on_submit():
        used: Stock = Stock.query.get(use_product_form.stock.data)
        quantity = use_product_form.quantity.data
        if quantity <= used.quantity:
            price_per_unit = used.price / used.quantity
            used.quantity -= quantity
            used.status = 'у вжитку' if used.quantity > 0 else 'fully-used'
            used.price = round(used.quantity * price_per_unit, 2)
            db.session.commit()
            flash('Продукт використано')
        else:
            flash('Нема стільки продукту')
        return render_template('stock.html', form=form, products=products, title='Мої продукти',
                               all_products=all_products, trash=trash_sum, use_product_form=use_product_form)
    return render_template('stock.html', form=form, products=products, title='Мої продукти',
                           all_products=all_products, trash=trash_sum, use_product_form=use_product_form)


def select_query():
    """Helper function to generate SelectField choices"""
    choices = []
    query = ProductsCategory.query.all()
    for q in query:
        choices.append((q.id, q.name))
    return choices


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.category.choices = select_query()
    if form.validate_on_submit():
        entry = Product(name=form.name.data, kcal=form.kcal.data,
                        proteins=form.proteins.data, fats=form.fats.data,
                        carbs=form.carbs.data, fibers=form.fibers.data,
                        category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash('Продукт додано', category='success')

    return render_template('add_product.html', form=form)


@app.route('/full_use/<int:id>')
def full_use(id):
    entry: Stock = Stock.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Продукт повністю використано!')
    return redirect(url_for('stock'))


@app.route('/throw_away/<int:id>')
def throw_away(id):
    entry: Stock = Stock.query.get(id)
    trash: Trash = Trash(product_id=entry.product_id, quantity=entry.quantity,
                         measure=entry.measure, price=entry.price, user_id=current_user.id)
    db.session.add(trash)
    db.session.delete(entry)
    db.session.commit()
    flash("Продукт викинуто")
    return redirect(url_for('stock'))


@app.route('/product/<int:id>')
def product_info(id):
    product = Product.query.get_or_404(id)
    return render_template('product_info.html', product=product)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')


if __name__ == '__main__':
    app.run(debug=True)
