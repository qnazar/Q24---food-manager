from application import db


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    time = db.Column(db.Integer)
    complexity = db.Column(db.String(32))
    description = db.Column(db.Text)
    instruction = db.Column(db.Text)
    picture = db.Column(db.String)

    ingredient = db.relationship('Ingredient', backref='recipe', lazy=True)

    def __str__(self):
        return self.name


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Float())
    measure = db.Column(db.String(16))
