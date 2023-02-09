from celery.schedules import crontab


CELERY_IMPORTS = ('application.auth.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'testing_celery_beat': {
        'task': 'application.auth.tasks.testing_celery_beat',
        'schedule': crontab(minute="*"),
    }
}
