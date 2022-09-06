from celery import shared_task
from django.core.mail import send_mail
from .models import NewsletterEmail
from django.conf import settings


@shared_task
def newsletter_subscription_email_task(email: str) -> int:
    """Task to send email on newsletter subscription"""

    subject = 'Спасибо, что подписались на нашу рассылку.'
    message = 'Здравствуйте, спасибо, что подписались на нашу email-рассылку, мы будем отправлять вам письма ' \
              'с различными предложениями и акциями. Приятного вам аппетита!'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return mail_sent


@shared_task
def newsletter_email_task():
    """Task to send newsletter to user emails"""
    email_list = [email for email in NewsletterEmail.objects.all().only('email')]
    subject = 'Сообщение с акциями.'
    message = """Только сейчас в Ninja Sushi стартует новая акция: закажи 2 ролла калифорния и получи 3-ий в подарок.
Успей купить!"""
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, email_list)
    return mail_sent
