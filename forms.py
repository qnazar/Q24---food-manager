from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, DateField, IntegerField, \
    FloatField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, Regexp


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))


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
    weight = MyFloatField("Вага (кг) 00.0")
    height = IntegerField("Зріст (см)")
    constitution = SelectField('Тип статури', choices=[('Normostenic', 'Нормостенік'),
                                                       ('Astenic', 'Астенік'),
                                                       ('Hyperstenic', 'Гіперстенік')])
    activity = MyFloatField("Коефіцієнт активності 0.000")
    submit = SubmitField('Підтвердити')


class ProfilePicForm(FlaskForm):
    profile_pic = FileField('Аватарка')
    submit = SubmitField('Змінити')


class CalcForm(FlaskForm):
    weight = MyFloatField("Вага (кг) 00.0")
    submit = SubmitField('Отримати результат')


class StockForm(FlaskForm):
    name = StringField("Назва продукту")
    quantity = MyFloatField("Кількість")
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    produced_date = DateField("Дата виготовлення")
    expired_date = DateField("Вжити до")
    price = MyFloatField("Ціна")
    submit = SubmitField('Додати')


# class UseFromStockForm(FlaskForm):
#     name = SelectField('Продукт')
#     full = BooleanField('Повністю')
#     quant = MyFloatField('Кількість')
#     submit = SubmitField('Використати')


class ProductForm(FlaskForm):
    name = StringField("Назва")
    category = SelectField('Категорія')
    kcal = IntegerField("Калорійність")
    proteins = MyFloatField("Білки")
    fats = MyFloatField("Жири")
    carbs = MyFloatField("Вуглеводи")
    fibers = MyFloatField("Клітковина")
    submit = SubmitField("Додати")


class UseProductForm(FlaskForm):
    quantity = MyFloatField('Кількість')
    submit = SubmitField('Використати')
