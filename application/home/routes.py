from flask import Blueprint, render_template, session

home_bp = Blueprint('home_bp', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/home/static')


@home_bp.before_app_first_request
def before_first_request():
    session.permanent = True


@home_bp.route('/')
def index():
    return render_template('home.html', title='Home')


@home_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@home_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html')
