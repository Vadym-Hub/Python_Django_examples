from django.db import models
from django.utils import timezone 
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """Собственный менеджер для получения всех опубликованных статей."""
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model): 
    """Модель статьи."""
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title = models.CharField(max_length=250, verbose_name='заголовок') 
    slug = models.SlugField(max_length=250,  
                            unique_for_date='publish') 
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_posts') 
    body = models.TextField(verbose_name='содержание') 
    publish = models.DateTimeField(default=timezone.now, verbose_name='дата публикации') 
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания') 
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления') 
    status = models.CharField(max_length=10,  
                              choices=STATUS_CHOICES, 
                              default='draft',
                              verbose_name='статус') 
    
    objects = models.Manager()  # Менеджер по умолчанию.
    published = PublishedManager()   # Наш новый менеджер.
    tags = TaggableManager()

    class Meta: 
        ordering = ('-publish',)
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80, verbose_name='имя')
    email = models.EmailField() 
    body = models.TextField(verbose_name='содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    active = models.BooleanField(default=True, verbose_name='активно')
 
    class Meta: 
        ordering = ('created',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
 
    def __str__(self): 
        return f'Комментарий от {self.name} к {self.post}'
