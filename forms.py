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
    email = EmailField('Електронна адреса', validators=[DataRequired()])  # TODO email validator
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                     Length(5, 20, message="Pw should be at list %(min)d symbols"),
                                                     EqualTo('password_confirm', message="Passwords  need to match!")])
    password_confirm = PasswordField('Підтвердежння пароля', validators=[DataRequired()])
    submit = SubmitField('Зареєструватися')


class LoginForm(FlaskForm):
    email = EmailField('Електронна адреса', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')


class ProfileForm(FlaskForm):
    first_name = StringField("Ім’я", validators=[Length(max=128)])
    last_name = StringField("Прізвище", validators=[Length(max=128)])
    sex = SelectField("Стать", choices=[('Чоловіча', 'Чоловіча'), ('Жіноча', 'Жіноча')])
    birthday = DateField("Дата народження", validators=[DataRequired()])
    weight = MyFloatField("Вага", validators=[DataRequired()])
    height = IntegerField("Зріст", validators=[DataRequired()])
    constitution = SelectField('Тип статури', choices=[('Нормостенік', 'Нормостенік'),
                                                       ('Астенік', 'Астенік'),
                                                       ('Гіперстенік', 'Гіперстенік')])
    activity = MyFloatField("Коефіцієнт активності", default=1.2, validators=[DataRequired()])
    submit = SubmitField('Підтвердити')


class ProfilePicForm(FlaskForm):
    profile_pic = FileField('Аватарка')
    submit = SubmitField('Змінити')


class StockForm(FlaskForm):
    name = StringField("Назва")
    quantity = MyFloatField("Кількість")
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    produced_date = DateField("Дата виготовлення")
    expired_date = DateField("Вжити до")
    price = MyFloatField("Ціна")
    submit = SubmitField('Додати')


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
    stock = StringField('Продукт')
    quantity = MyFloatField('Кількість')
    submit = SubmitField('Використати')
