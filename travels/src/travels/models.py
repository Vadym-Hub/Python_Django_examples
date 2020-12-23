from django.db import models
from django.core.exceptions import ValidationError


class City(models.Model):
    """Модель города."""
    name = models.CharField(
        max_length=100, unique=True, verbose_name='город'
    )

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        ordering = ['name']

    def __str__(self):
        return self.name


class Train(models.Model):
    """Модель поезда."""
    name = models.CharField(
        max_length=50, unique=True, verbose_name='номер поезда'
    )
    travel_time = models.PositiveSmallIntegerField(
        verbose_name='время в пути'
    )
    from_city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='from_city_set',
        verbose_name='из какого города'
    )
    to_city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='to_city_set',
        verbose_name='в какой город'
    )

    class Meta:
        verbose_name = 'поезд'
        verbose_name_plural = 'поезда'
        ordering = ['travel_time']

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Изменить город прибытия')
        qs = Train.objects.filter(
            from_city=self.from_city, to_city=self.to_city,
            travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Измените время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Поезд №{self.name} из города {self.from_city}'


class Route(models.Model):
    """Модель маршрута."""
    name = models.CharField(
        max_length=50, unique=True, verbose_name='название маршрута'
    )
    travel_times = models.PositiveSmallIntegerField(
        verbose_name='общее время в пути'
    )
    from_city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='route_from_city_set',
        verbose_name='из какого города'
    )
    to_city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='route_to_city_set',
        verbose_name='в какой город'
    )
    trains = models.ManyToManyField(
        Train,
        verbose_name='список поездов'
    )

    def __str__(self):
        return f'Маршрут {self.name} из города {self.from_city}'

    class Meta:
        verbose_name = 'маршрут'
        verbose_name_plural = 'маршруты'
        ordering = ['travel_times']
