from django.conf import settings
from django.core.mail import send_mail


def send_deactivate_email(user):
    send_mail(
        'Товар деактивирован',
        'Товар деактивирован. Обратитесь к администратору.',
        settings.EMAIL_HOST_USER,
        recipient_list=[user.name]

    )