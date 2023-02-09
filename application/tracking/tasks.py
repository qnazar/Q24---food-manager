import os

from celery import shared_task
from flask_mail import Message

from application import mail
from application.profile.models import Profile


@shared_task
def daily_stock():
    queryset = Profile.query.filter_by(daily_stock_subscription=True).all()
    for profile in queryset:
        email = profile.user.email
        header = 'Ваш запас продуктів на сьогодні:\n'
        stock = '\n'.join([f'{item.product.name}: {item.quantity}{item.measure} до {item.expired}' for item in profile.user.stock])
        footer = '\nВаш Q24'
        message = Message('Денний запас', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
        message.body = header + stock + footer
        mail.send(message=message)
