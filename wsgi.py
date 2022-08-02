from flask import Flask, render_template, request, url_for, g, flash, get_flashed_messages
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from Database import Database
from credentials import SECRET_KEY
from User import User
from DBUser import DBUser
from texts_ua import Texts
from forms import RegisterForm


app = Flask(__name__)
app.config.from_pyfile('credentials.py')
app.config['SECRET_KEY'] = SECRET_KEY

mail = Mail(app)

s = URLSafeTimedSerializer('SomethingSecret')


@app.before_request
def get_db():
    """Getting DB before start of the session"""
    if not hasattr(g, 'db'):
        g.db = Database()


@app.teardown_appcontext
def close_contest(error):
    """Closing DB after session"""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/calc')
def calc():
    return render_template('calc.html', title='Calc')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    password=form.password.data)

        dbUser = DBUser(user, g.db)
        if dbUser.can_be_created:
            result = dbUser.create()
            if result is True:
                flash(Texts.reg_success)
            else:
                flash(Texts.reg_fail)
        else:
            flash(Texts.reg_fail)

        form.email.data = ''
    return render_template('registration.html', title='Registration', form=form)


@app.route('/confirm_email/<token>')
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=30)
    except SignatureExpired:
        return "Failed"
    return 'All worked'  # тут я можу повернути авторизовану сторінку або краще редірект


@app.route('/user/<id>')
def user(id):
    return f"<h1>Hello {id}</h1>"


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
