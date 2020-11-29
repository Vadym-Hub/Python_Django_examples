from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категорії"""
    name = models.CharField('Категорія', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Продукт', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField('Фото', upload_to='products/')
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Кількість')
    available = models.BooleanField('В наявності', default=True)
    created = models.DateTimeField('Дата створення', auto_now_add=True)
    updated = models.DateTimeField('Дата оновлення', auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def get_absolute_url(self):
        return reverse('shops:product_detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
