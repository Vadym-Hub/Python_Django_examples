# Generated by Django 3.1 on 2020-08-18 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-created',), 'verbose_name': 'новостна лента', 'verbose_name_plural': 'новостных лент'},
        ),
    ]