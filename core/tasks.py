from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email(user_email, verification_link):
    subject = 'لینک تایید ایمیل شما'
    message = f'سلام!\nلطفاً برای تایید ایمیل خود روی لینک زیر کلیک کنید:\n{verification_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def send_password_reset_email(user_email, reset_link):
    subject = 'Reset Your Password'
    message = f'Hi!\nClick the link below to reset your password:\n{reset_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
