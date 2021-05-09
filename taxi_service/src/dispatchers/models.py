from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """
    Кастомизированая модель пользователя.
    """
    pass

    class Meta:
        verbose_name = 'диспетчер'
        verbose_name_plural = 'диспетчера'


class Car(models.Model):
    """
    Модель машины.
    """
    brand = models.CharField('модель машины', max_length=50)
    is_busy = models.BooleanField('машина занята', default=False)

    class Meta:
        verbose_name = 'машина'
        verbose_name_plural = 'машины'

    def __str__(self):
        return self.brand

    def car_to_pool(self):
        self.is_busy = False
        self.save()
        return reverse('dispatchers:car_list')
