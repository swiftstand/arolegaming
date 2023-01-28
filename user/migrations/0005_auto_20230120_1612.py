# Generated by Django 3.2.7 on 2023-01-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20230101_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.AddField(
            model_name='dragprofile',
            name='city',
            field=models.TextField(default='input address'),
        ),
        migrations.AddField(
            model_name='dragprofile',
            name='social_links',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='dragprofile',
            name='tip_url',
            field=models.URLField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.CharField(editable=False, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='dragprofile',
            name='availability',
            field=models.BooleanField(default=True),
        ),
    ]
