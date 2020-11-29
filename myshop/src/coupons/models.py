from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """Модель скидочного купона"""
    code = models.CharField(max_length=50, unique=True, verbose_name='код купона')
    valid_from = models.DateTimeField(verbose_name='дата и время начала действия купона')
    valid_to = models.DateTimeField(verbose_name='дата и время окончания действия купона')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='размер скидки в %')
    active = models.BooleanField(verbose_name='активен')

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'купоны'

    def __str__(self):
        return self.code
