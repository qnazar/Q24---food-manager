from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, DateField, IntegerField, \
    FloatField, DecimalField
from wtforms.validators import Email, DataRequired, Length, EqualTo, Regexp


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
    sex = SelectField("Стать", choices=[('Male', 'Чоловіча'), ('Female', 'Жіноча')])
    birthday = DateField("Дата народження", validators=[DataRequired()])
    weight = FloatField("Вага (кг) 00.0")
    height = IntegerField("Зріст (см)")
    constitution = SelectField('Тип статури', choices=[('Normostenic', 'Нормостенік'),
                                                       ('Astenic', 'Астенік'),
                                                       ('Hyperstenic', 'Гіперстенік')])
    activity = FloatField("Коефіцієнт активності 0.000")
    submit = SubmitField('Підтвердити')


class ProfilePicForm(FlaskForm):
    profile_pic = FileField('Аватарка')
    submit = SubmitField('Змінити')


class CalcForm(FlaskForm):
    weight = FloatField("Вага (кг) 00.0")
    submit = SubmitField('Отримати результат')


class StockForm(FlaskForm):
    name = StringField("Назва продукту")
    quantity = FloatField("Кількість")
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    produced_date = DateField("Дата виготовлення")
    expired_date = DateField("Вжити до")
    price = FloatField("Ціна")
    submit = SubmitField('Додати')
