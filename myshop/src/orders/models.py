from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

from shop.models import Product
from coupons.models import Coupon


class Order(models.Model):
    """Модель заказа"""
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='e-mail')
    address = models.CharField(max_length=250, verbose_name='адресс')
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100, verbose_name='город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='время оформления')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменено')
    paid = models.BooleanField(default=False, verbose_name='оплачено')
    braintree_id = models.CharField(max_length=150, blank=True, verbose_name='идентификатор транзакции')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='купон')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_total_cost(self):
        """Чтобы получить общую стоимость товаров в заказе."""
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    """Модель для связи заказа с покупаемыми товарами и указания их стоимости и количества."""
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        """Чтобы получить стоимость количества товара."""
        return self.price * self.quantity

    def __str__(self):
        return f'{self.id}'
