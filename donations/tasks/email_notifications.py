from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from donations.models import Collect, Payment


@shared_task
def send_collect_created_email(collect_id):
    collect = Collect.objects.select_related("author").get(id=collect_id)
    subject = f"Ваш сбор '{collect.title}' создан"
    message = (
        f"Здравствуйте, {collect.author.username}!\n\n"
        f"Сбор '{collect.title}' успешно создан.\n"
        f"Цель: {collect.goal_amount or 'Бессрочный'}\n"
        f"Дата окончания: {collect.ends_at.strftime('%d.%m.%Y')}"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [collect.author.email])


@shared_task
def send_payment_created_email(payment_id):
    payment = Payment.objects.select_related("donator", "collect").get(id=payment_id)
    subject = "Спасибо за пожертвование!"
    message = (
        f"Здравствуйте, {payment.donator.username}!\n\n"
        f"Вы пожертвовали {payment.amount} руб. на сбор '{payment.collect.title}'.\n"
        f"Спасибо за вашу поддержку!"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [payment.donator.email])
