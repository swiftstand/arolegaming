# Generated by Django 3.2.7 on 2023-02-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_alter_dragevent_raw_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dragevent',
            name='raw_date',
            field=models.IntegerField(default=0),
        ),
    ]
