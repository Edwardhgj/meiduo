# Generated by Django 2.1.4 on 2019-09-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20190905_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='code',
            field=models.CharField(default='', max_length=100),
        ),
    ]
