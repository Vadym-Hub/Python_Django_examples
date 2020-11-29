from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from .fields import OrderField


# Subject 1
#     Course 1
#         Module 1
#             Content 1 (image)
#             Content 2 (text)
#         Module 2
#             Content 3 (text)
#             Content 4 (file)
#             Content 5 (video)
#             ...


class Subject(models.Model):
    """Модель предмета"""
    title = models.CharField(max_length=200, verbose_name='название предмета')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self):
        return self.title


class Course(models.Model):
    """Модель курса"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses_created',
                              on_delete=models.CASCADE, verbose_name='преподаватель')
    subject = models.ForeignKey(Subject, related_name='courses',
                                on_delete=models.CASCADE, verbose_name='предмет')
    title = models.CharField(max_length=200, verbose_name='название курса')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(verbose_name='описание курса')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания курса')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_joined',
                                      blank=True, verbose_name='студенты')

    class Meta:
        ordering = ['-created']
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Module(models.Model):
    """Модель модуля курса"""
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='курс')
    title = models.CharField(max_length=200, verbose_name='название модуля')
    description = models.TextField(blank=True, verbose_name='описание модуля')
    order = OrderField(blank=True, for_fields=['course'])  # Поле со своим придуманным классом

    class Meta:
        ordering = ['order']
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """Модель содержимого курсов"""
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name='модуль')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     verbose_name='внешний ключ',
                                     limit_choices_to={'model__in': ('text',
                                                                     'video',
                                                                     'image',
                                                                     'file')})
    object_id = models.PositiveIntegerField(verbose_name='идентификатор связанного объекта')
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])  # Поле со своим придуманным классом

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """Абстрактная модель для связей содержимого модуля курса"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        """Отображение страницы с содержимым курса в зависимости от типа"""
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})

    def __str__(self):
        return self.title


class Text(ItemBase):
    """Модель текста для модуля курса"""
    content = models.TextField()


class File(ItemBase):
    """Модель файла для модуля курса"""
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Модель изображения для модуля курса"""
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """Модель видео для модуля курса"""
    url = models.URLField()
