import os

from flask_mail import Message
from celery import shared_task

from application import mail


@shared_task
def send_registration_email(email, link):
    msg = Message('Confirm email', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
    msg.body = f'Your link is {link}'
    mail.send(msg)


@shared_task
def testing_celery_beat():
    print('CELERY BEAT IS WORKING. EVERY MINUTE')
