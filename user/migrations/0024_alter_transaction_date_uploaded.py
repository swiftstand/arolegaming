# Generated by Django 3.2.7 on 2023-04-24 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20230424_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 11, 51, 28, 360169), verbose_name='date made'),
        ),
    ]