from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def order_created_email_task(order_id: int) -> int:
    """Task to send email on successful ordering"""

    order = Order.objects.get(id=order_id)
    order_list = [f'{index + 1}. Название: {item.product.name}, Цена: {item.product.price}₽, '
                  f'Количество: {item.quantity} шт. Общая цена: {item.product.price * item.quantity}₽.'
                  for index, item in enumerate(order.items.all())]
    order_list_text = '\n'.join(order_list)
    subject = f'Успешный заказ №{order_id}'
    message = f'''Дорогой {order.name}, ваш заказ №{order_id} был успешно создан. В ближайшее время ваш заказ ''' \
              f'''доставит курьер. 
Состав заказа: 
{order_list_text}

Итоговая стоимость заказа: {order.get_total_cost()}₽.'''

    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [order.email])
    return mail_sent
