import logging
from celery import shared_task
from django.core.mail import send_mail
from Snappfood import settings

@shared_task(bind=True)
def send_notification_mail(self, target_mail, message):
    mail_subject = "Welcome on Board!"
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        auth_password=settings.EMAIL_HOST_PASSWORD,
        fail_silently=False,
        )
    return "Done"
