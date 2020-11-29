# Асинхронные задачи для Celery
from celery import task
from django.core.mail import send_mail

from .models import Order


@task
def order_created(order_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Уважаемый {order.first_name},\n\nВы успешно оформили заказ.\
                Ваш заказ №: {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent
