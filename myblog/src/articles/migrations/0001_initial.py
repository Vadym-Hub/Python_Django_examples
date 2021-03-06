# Generated by Django 3.0.8 on 2020-07-29 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='название статьи')),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('text', models.TextField(verbose_name='текст статьи')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата публикации')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('status', models.CharField(choices=[('черновик', 'Черновик'), ('опубликовано', 'Опубликковано')], default='черновик', max_length=13, verbose_name='статус')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='автор', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='категория', to='articles.Category')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
                'ordering': ('-publish',),
            },
        ),
    ]
