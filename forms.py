from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])  # TODO email validator
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(5, 20, message="Pw should be at list %(min)d symbols"),
                                                     EqualTo('password_confirm', message="Passwords  need to match!")])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProfileForm(FlaskForm):
    first_name = StringField("Ім’я", validators=[Length(max=128)])
    last_name = StringField("Прізвище", validators=[Length(max=128)])
    sex = SelectField("Стать", choices=[('M', 'M'), ('F', 'Ж')])
    birthday = DateField("Дата народження", validators=[DataRequired()])
    profile_pic = FileField('Аватарка')
    submit = SubmitField('Submit')
