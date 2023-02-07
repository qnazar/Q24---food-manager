from flask import Blueprint

profile_bp = Blueprint('profile_bp', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/profile/static')

from . import routes
