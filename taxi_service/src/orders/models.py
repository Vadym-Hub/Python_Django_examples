from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from dispatchers.models import Car


class Order(models.Model):
    """
    Модель заказа.
    """
    name = models.CharField('имя', max_length=50)
    phone = models.CharField('телефон', max_length=17)
    address_from = models.CharField('адрес заказа', max_length=60)
    destination = models.CharField('адрес следования', max_length=60)
    desired_time = models.TimeField('желаемое время подачи авто')
    car = models.ForeignKey(
        Car,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='свободная машина'
    )
    created = models.DateTimeField('время оформления', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Заказ №{self.id}'
