# Generated by Django 2.1.4 on 2019-09-05 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_orders_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_sn',
            field=models.CharField(max_length=180, unique=True),
        ),
    ]
