# Generated by Django 3.2 on 2021-04-28 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dispatchers', '0003_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='имя')),
                ('phone', models.CharField(max_length=15, verbose_name='телефон')),
                ('address_from', models.CharField(max_length=60, verbose_name='адрес заказа')),
                ('destination', models.CharField(max_length=60, verbose_name='адрес следования')),
                ('desired_time', models.TimeField(verbose_name='желаемое время')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='время оформления')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='dispatchers.car', verbose_name='свободная машина')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ('-created',),
            },
        ),
    ]
