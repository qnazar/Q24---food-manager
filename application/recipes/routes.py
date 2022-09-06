import os
import uuid
from flask import Blueprint, render_template, abort, request, flash
from werkzeug.utils import secure_filename
from application import db
from models import Recipe, Ingredient, Product
from forms import RecipeForm, IngredientForm

recipes_bp = Blueprint('recipes_bp', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/recipes/static')


@recipes_bp.route('/recipes', methods=['GET', 'POST'])
def recipes():
    all_recipes = Recipe.query.all()
    return render_template('recipes.html', title='Рецепти', recipes=all_recipes)


@recipes_bp.route('/recipe/<int:id>')
def recipe_info(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        abort(404)
    return render_template("recipe.html", title=recipe.name, recipe=recipe)


@recipes_bp.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
    all_products = Product.query.all()
    all_recipes = Recipe.query.all()
    recipe_form = RecipeForm()
    ingredient_form = IngredientForm()
    if recipe_form.validate_on_submit() and recipe_form.submit.data:

        picture = request.files['picture']
        pic_filename = secure_filename(picture.filename)
        pic_name = str(uuid.uuid1()) + '_' + pic_filename
        picture.save(os.path.join(recipes_bp.static_folder, 'images/recipes/', pic_name))

        new_rec = Recipe(name=recipe_form.name.data,
                         time=recipe_form.time.data,
                         complexity=recipe_form.complexity.data,
                         description=recipe_form.description.data,
                         instruction=recipe_form.instruction.data,
                         picture=pic_name)
        db.session.add(new_rec)
        db.session.commit()
        flash('Рецепт додано')
    if ingredient_form.validate_on_submit() and ingredient_form.add.data:
        recipe_id = Recipe.query.filter_by(name=ingredient_form.recipe.data).first().id
        product_id = Product.query.filter_by(name=ingredient_form.product.data).first().id
        ingred = Ingredient(recipe_id=recipe_id,
                            product_id=product_id,
                            quantity=ingredient_form.quantity.data,
                            measure=ingredient_form.measure.data)
        db.session.add(ingred)
        db.session.commit()
        flash('Інгредієнт додано')
    return render_template('add_recipe.html', recipe_form=recipe_form, ingredient_form=ingredient_form,
                           all_products=all_products, all_recipes=all_recipes)
