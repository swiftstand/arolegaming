# Generated by Django 3.2.7 on 2023-01-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20230120_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dragprofile',
            name='city',
            field=models.TextField(default='input address', editable=False),
        ),
        migrations.AlterField(
            model_name='dragprofile',
            name='social_links',
            field=models.CharField(editable=False, max_length=1000, null=True),
        ),
    ]
