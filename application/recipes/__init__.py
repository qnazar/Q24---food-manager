from flask import Blueprint

recipes_bp = Blueprint('recipes_bp', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/recipes/static')

from . import routes
