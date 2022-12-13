from application import celery, init_app
from celery_utils import init_celery


app = init_app(celery=celery)
init_celery(celery, app)
