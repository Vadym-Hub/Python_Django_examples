from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class Category(models.Model):
    """Модель категорий статей"""
    name = models.CharField('категория', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель статьи"""
    STATUS_CHOICES = (
        ('черновик', 'Черновик'),
        ('опубликовано', 'Опубликковано'),
    )
    author = models.ForeignKey(User, verbose_name='автор', on_delete=models.SET_NULL, blank=False, null=True)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.SET_NULL, null=True)
    title = models.CharField('название статьи', max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    text = models.TextField('текст статьи')
    publish = models.DateTimeField('дата публикации', default=timezone.now)
    created = models.DateTimeField('дата создания', auto_now_add=True)
    updated = models.DateTimeField('дата обновления', auto_now=True)
    status = models.CharField('статус', max_length=13, choices=STATUS_CHOICES, default='черновик')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)  # сортировка статей в обратном порядке
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def get_comment(self):
        """метод возврата комментариек к статье"""
        return self.comment_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        """Метод выводу статьи по slug"""
        return reverse('articles:article_detail', args=[self.publish.year, self.publish.month,
                                                        self.publish.day, self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментариев к статье"""
    article = models.ForeignKey(Article, verbose_name='статья', on_delete=models.CASCADE)
    author_name = models.CharField('имя автора', max_length=50)
    comment_text = models.CharField('текст комментария', max_length=5000)
    created = models.DateTimeField('дата создания', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'комментар'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.author_name} - {self.article}'
