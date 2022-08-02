from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])  # TODO email validator
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(5, 20, message="Pw should be at list %(min)d symbols")])
    submit = SubmitField('Submit')
