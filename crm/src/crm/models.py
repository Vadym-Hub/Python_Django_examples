from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True, verbose_name='является ли главой организации crm')  # app CRM
    is_agent = models.BooleanField(default=False, verbose_name='является ли агентом crm')  # app CRM


class Organisation(models.Model):
    """
    Модель организации.
    Зарегестрировынный User одновременно является организацией.
    Возвращает user.username как название организации.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='глава организации',
    )

    class Meta:
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return self.user.username


class Agent(models.Model):
    """
    Модель агента по продажам.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name='организация'
    )

    class Meta:
        verbose_name = 'агент по продажам'
        verbose_name_plural = 'агенты по продажам'

    def __str__(self):
        return self.user.get_full_name()


class Lead(models.Model):
    """
    Модель лида.
    """

    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_CONVERTED = 'converted'
    STATUS_UNCONVERTED = 'unconverted'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_CONTACTED, 'Связались'),
        (STATUS_CONVERTED, 'Согласен'),
        (STATUS_UNCONVERTED, 'Отказано'),
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name='организация'
    )
    agent = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='личный агент'
    )
    status = models.CharField('статус', max_length=30, choices=STATUS_CHOICES, default=STATUS_NEW)
    first_name = models.CharField('имя', max_length=20)
    last_name = models.CharField('фамилия', max_length=20)
    age = models.IntegerField('возраст')
    phone_number = models.CharField('номер телефона', max_length=12)
    email = models.EmailField('e-mail')
    description = models.TextField('описание')
    date_added = models.DateTimeField('дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'лид'
        verbose_name_plural = 'лиды'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def post_user_created_signal(sender, instance, created, **kwargs):
    """
    Если User был создан, автоматически создает Organisation.
    """
    if created:
        Organisation.objects.create(user=instance)


# Создается сигнал про то, что User создан.
post_save.connect(post_user_created_signal, sender=settings.AUTH_USER_MODEL)
