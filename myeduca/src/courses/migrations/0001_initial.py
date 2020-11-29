# Generated by Django 3.1 on 2020-08-10 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название курса')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('overview', models.TextField(verbose_name='описание курса')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания курса')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to=settings.AUTH_USER_MODEL, verbose_name='преподаватель')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название предмета')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'предмет',
                'verbose_name_plural': 'предметы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название раздела')),
                ('description', models.TextField(blank=True, verbose_name='описание раздела')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'раздел',
                'verbose_name_plural': 'разделы',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.subject', verbose_name='предмет'),
        ),
    ]