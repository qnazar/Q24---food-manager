from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, DateField, IntegerField, \
    FloatField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))


class RegisterForm(FlaskForm):
    email = EmailField('Електронна адреса', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                                   Length(5, 20, message="Pw should be at list %(min)d symbols"),
                                                   EqualTo('password_confirm', message="Passwords  need to match!")])
    password_confirm = PasswordField('Підтвердження пароля', validators=[DataRequired()])
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
    weight = DecimalField("Вага", validators=[DataRequired(), NumberRange(min=30, max=200)])
    height = IntegerField("Зріст", validators=[DataRequired(), NumberRange(min=100, max=220)])
    constitution = SelectField('Тип статури', choices=[('Нормостенік', 'Нормостенік'),
                                                       ('Астенік', 'Астенік'),
                                                       ('Гіперстенік', 'Гіперстенік')])
    activity = DecimalField("Коефіцієнт активності", default=1.2, validators=[DataRequired(), NumberRange(min=1, max=2)])
    submit = SubmitField('Підтвердити')


class ProfilePicForm(FlaskForm):
    profile_pic = FileField('Аватарка')
    submit = SubmitField('Змінити')


class StockForm(FlaskForm):
    name = StringField("Назва", validators=[DataRequired()])
    quantity = DecimalField("Кількість", validators=[DataRequired()])
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    produced_date = DateField("Дата виготовлення", validators=[DataRequired()])
    expired_date = DateField("Вжити до", validators=[DataRequired()])
    price = DecimalField("Ціна", validators=[DataRequired()])
    add = SubmitField('Додати')


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
    stock = StringField('Продукт', validators=[DataRequired()])
    quantity = DecimalField('Кількість', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Використати')


class ShoppingForm(FlaskForm):
    name = StringField("Назва")
    quantity = MyFloatField("Кількість")
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    submit = SubmitField('Додати')


class TrashFilterForm(FlaskForm):
    choice = SelectField('Період', choices=[('day', 'Сьогодні'), ('week', 'Тиждень'),
                                            ('month', 'Місяць'), ('year', 'Рік')])
    submit = SubmitField('Показати')


class RecipeForm(FlaskForm):
    name = StringField("Назва")
    time = IntegerField("Час приготування")
    complexity = SelectField("Складність", choices=[('легко', 'легко'), ('середнє', 'середнє'), ('важко', 'важко')])
    description = TextAreaField("Опис")
    instruction = TextAreaField("Інструкція")
    picture = FileField("Фото")
    submit = SubmitField("Додати")


class IngredientForm(FlaskForm):
    recipe = StringField('Рецепт')
    product = StringField("Продукт")
    quantity = MyFloatField("Кількість")
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    add = SubmitField("Додати")


class ProductsForMealForm(FlaskForm):

    product = StringField('Продукт', validators=[DataRequired()])
    quantity = MyFloatField('Кількість', validators=[DataRequired()])
    measure = SelectField("Міра", choices=[('г', 'г'), ('кг', 'кг'), ('шт', 'шт'), ('мл', 'мл'), ('л', 'л')])
    add = SubmitField('Додати')


class AddMealForm(FlaskForm):
    meal = SelectField("Прийом", choices=[('Сніданок', 'Сніданок'), ('Обід', 'Обід'),
                                          ('Вечеря', 'Вечеря'), ('Перекус', 'Перекус')])
    name = StringField('Назва страви', default='Без назви')
    submit = SubmitField('Додати')
    clear = SubmitField('Очистити')
