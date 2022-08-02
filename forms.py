from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
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
