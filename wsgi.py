from flask import Flask, render_template, url_for, flash, redirect
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user

from models import db, User
from config import *
from texts_ua import Texts
from forms import RegisterForm, LoginForm


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{PG_USER}:{PG_PSSWRD}@localhost/{PG_DATABASE}"
db.init_app(app)
mail = Mail(app)
s = URLSafeTimedSerializer('SomethingSecret')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def get_db():
    """Getting DB before start of the session"""
    db.create_all()


@app.teardown_appcontext
def close_contest(error):
    """Closing DB after session"""
    db.close_all_sessions()


@app.route('/')
def index():
    return render_template('home.html', title='Home')


# @app.route('/calc')
# def calc():
#     return render_template('calc.html', title='Calc')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user is None:

            user = User(email=form.email.data,
                        password_hash=generate_password_hash(form.password.data))

            db.session.add(user)
            db.session.commit()
            flash(Texts.reg_success)
            return redirect(location=url_for('user', id=user.id))
        else:
            flash('This email is already used')

        # if user.id:
        #     flash(Texts.reg_success)
        #     return redirect(location=url_for('user', id=user.id))  #
        # else:
        #     flash(Texts.reg_fail)

        form.email.data = ''
    return render_template('registration.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login successfully')
                return redirect(url_for('user', id=user.id))
            else:
                flash('Неправильний пароль')
        else:
            flash('Немає користувача з такою електронною адресою')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logout')
    return redirect(url_for('login'))

@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    return render_template('user.html', title='Profile', user=user)


@app.route('/confirm_email/<token>')
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=30)
    except SignatureExpired:
        return "Failed"
    return 'All worked'  # тут я можу повернути авторизовану сторінку або краще редірект


@app.route('/send')
def send():

    email = 'qnazar@ukr.net'
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm email', sender=app.config['MAIL_USERNAME'], recipients=[email])

    link = url_for('confirm', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    return "<h1>Message sent</h1>"


if __name__ == '__main__':
    app.run(debug=True)
