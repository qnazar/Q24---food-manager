from flask import Blueprint

tracking_bp = Blueprint('tracking_bp', __name__, template_folder='templates',
                        static_folder='static', static_url_path='/tracking/static')

from . import routes
