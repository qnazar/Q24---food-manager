from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import uuid
import os

from models import db, User, Profile
from texts_ua import Texts
from forms import RegisterForm, LoginForm, ProfileForm, ProfilePicForm, WaterForm

app = Flask(__name__)
app.config.from_pyfile('config.py')

# DB initialization
db.init_app(app)
with app.app_context():
    db.create_all()

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
            user = User(email=form.email.data,
                        password_hash=generate_password_hash(form.password.data))
            # adding user to the db
            db.session.add(user)
            db.session.commit()
            login_user(user)  # autologin after registration
            flash(Texts.reg_success, category='success')

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
    flash('You have been logout', category='success')
    return redirect(url_for('login'))


@app.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    profile = Profile.query.get_or_None(id)
    if not profile:
        profile = Profile(id=current_user.id, user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    return render_template('user.html', title='Profile', user=current_user, person=profile)


@app.route('/user/<id>/update', methods=['GET', 'POST'])
def update_personal_info(id):
    person = current_user.person
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
        print(person.body_mass_index())
        print(person.basic_metabolism_rate())
        print(person.daily_kcal_intake())
        print(person.ideal_weight())
        print(person.water_norm())
        print(person.highest_normal_weight())
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
    return redirect(url_for('user', id=current_user.id))


@app.route('/calculations/<mode>', methods=['GET', 'POST'])
@login_required
def calculations(mode):
    if mode == 'water':
        form = WaterForm(weight=current_user.profile.weight)
        if form.validate_on_submit():
            current_user.profile.weight = form.weight.data
            db.session.commit()
            water = current_user.profile.water_norm()
            flash(f'Твоя денна норма води - {water} мл!')
            return redirect(url_for('user', id=current_user.id))
        return render_template('calculations.html', form=form, mode='water')
    elif mode == 'kcal':
        pass
    elif mode == 'imt':
        pass
    elif mode == 'weight':
        pass


if __name__ == '__main__':
    app.run(debug=True)
