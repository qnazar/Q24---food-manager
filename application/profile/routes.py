import os

from flask import render_template, redirect, abort, flash, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid

from application import db
from .models import Profile
from application.tracking.models import  Meal, Stock, ShoppingList, Trash
from application.forms import ProfileForm, ProfilePicForm
from application.helpers import stock_statistics
from application.profile import profile_bp


@profile_bp.route('/user/<int:id>', methods=['GET', 'POST'])
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
    shop_list = ShoppingList.query.filter_by(user_id=current_user.id).limit(3)
    meals = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.time.desc()).limit(5).all()
    return render_template('user.html', title='Profile', user=current_user, person=profile, stats=stats, trash=trash,
                           shop_list=shop_list, meals=meals)


@profile_bp.route('/user/<int:id>/update', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('profile_bp.user', id=current_user.id))
    return render_template('update.html', title='Update Info', user=current_user, form=form, person=person)


@profile_bp.route('/upload_picture', methods=['GET', 'POST'])
@login_required
def upload_picture():
    form = ProfilePicForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            if current_user.profile_pic:
                try:
                    os.remove(os.path.join(profile_bp.static_folder, 'images/profiles/', current_user.profile_pic))
                except FileNotFoundError:
                    pass
            picture = request.files['profile_pic']
            pic_filename = secure_filename(picture.filename)
            pic_name = str(uuid.uuid1()) + '_' + pic_filename

            picture.save(os.path.join(profile_bp.static_folder, 'images/profiles/', pic_name))
            current_user.profile_pic = pic_name
            db.session.commit()
            flash(message='Фото успішно оновлено', category='success')
        return redirect(url_for('profile_bp.user', id=current_user.id))
    return render_template('upload_picture.html', title='Upload profile pic', form=form)


@profile_bp.route('/delete_picture')
@login_required
def delete_picture():
    try:
        if current_user.profile_pic is None:
            pass
        else:
            os.remove(os.path.join(profile_bp.static_folder, 'images/profiles/', current_user.profile_pic))
            current_user.profile_pic = None
            db.session.commit()
            flash(message='Фото успішно видалено', category='success')
    except FileNotFoundError:
        flash('Проблема з фото')
    finally:
        return redirect(url_for('profile_bp.user', id=current_user.id))


@profile_bp.route('/calculations/<mode>', methods=['GET', 'POST'])
@login_required
def calculations(mode):
    if mode == 'about':
        return render_template('calculations.html')
    elif not current_user.profile.weight or not current_user.profile.height:
        flash('Потрібно вказати дані зросту та ваги!')
        return redirect(url_for('update_personal_info', id=current_user.id))
    elif mode == 'BMR':
        BMR = current_user.profile.basic_metabolism_rate()
        current_user.profile.BMR = BMR
        flash(f'Твій основний обмін - {BMR} ккал!')
    elif mode == 'BMI':
        BMI = current_user.profile.body_mass_index()
        current_user.profile.BMI = BMI
        flash(f'Твій індекс маси тіла - {BMI}!')
    elif mode == 'DKI':
        DKI = current_user.profile.daily_kcal_intake()
        current_user.profile.DKI = DKI
        flash(f'Твоя денна норма калорій - {DKI} ккал!')
    elif mode == 'DWN':
        DWN = current_user.profile.water_norm()
        current_user.profile.DWN = DWN
        flash(f'Твоя денна норма води - {DWN} мл!')
    elif mode == 'IW':
        min_weight = current_user.profile.min_normal_weight()
        max_weight = current_user.profile.max_normal_weight()
        med_weight = round((min_weight + max_weight) / 2, 1)
        current_user.profile.IW = med_weight
        current_user.profile.min_weight = min_weight
        current_user.profile.max_weight = max_weight
        flash(f'В ідеалі твоя вага повинна бути в межах {min_weight} - {max_weight} кг. Середня вага - {med_weight}кг.')
    db.session.commit()
    return redirect(url_for('profile_bp.calculations', mode='about'))
