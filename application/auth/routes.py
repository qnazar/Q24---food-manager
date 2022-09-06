import os
from flask import Blueprint, render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from itsdangerous import SignatureExpired

from application import mail, serializer, login_manager
from forms import RegisterForm, LoginForm
from models import db, User


auth_bp = Blueprint('auth_bp', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/auth/static')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/registration', methods=['GET', 'POST'])
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
            flash('Реєстрація пройшла успішно. Лист з підтвердженням відправлено на вашу електронну адресу',
                  category='success')

            # sending email confirmation
            token = serializer.dumps(user.email, salt='email-confirm')
            msg = Message('Confirm email', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
            link = url_for('auth_bp.confirm_email', token=token, _external=True)
            msg.body = f'Your link is {link}'
            mail.send(msg)

            return redirect(location=url_for('profile_bp.user', id=user.id))
        else:
            flash('Користувач з такою поштою вже існує', category='warning')
    return render_template('registration.html', title='Registration', form=form)


@auth_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=900)
        flash('Електронну пошту підтверджено!', category='success')
        current_user.email_confirmed = True
        db.session.commit()
    except SignatureExpired:
        return 'Signature time expired'
    return redirect(url_for('profile_bp.user', id=current_user.id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile_bp.user', id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Вітаємо з поверненням', category='success')
                return redirect(url_for('profile_bp.user', id=user.id))
            else:
                flash('Неправильний пароль', category='danger')
        else:
            flash('Немає користувача з такою електронною адресою', category='danger')
    return render_template('login.html', form=form, title='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('До зустрічі!', category='success')
    return redirect(url_for('auth_bp.login'))
