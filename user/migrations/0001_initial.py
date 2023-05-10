# Generated by Django 3.2.7 on 2023-05-06 19:44

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=100000, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('fullname', models.CharField(default='swift only', max_length=100)),
                ('is_drag_performer', models.BooleanField(default=False)),
                ('agreement', models.BooleanField(default=True, verbose_name='Drag4me terms and condion')),
                ('resetter', models.CharField(editable=False, max_length=100, null=True)),
                ('settings', models.CharField(editable=False, max_length=1000, null=True)),
                ('qr_id', models.CharField(max_length=1000, null=True)),
                ('pay_code', models.IntegerField(blank=True, default=1234, editable=False, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DragProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='user_default.png', upload_to='user_profile_pics', verbose_name='branch image')),
                ('about_me', models.TextField(blank=True, default='', null=True, verbose_name='branch description')),
                ('approved', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=False)),
                ('availability', models.BooleanField(default=True, editable=False)),
                ('website_url', models.CharField(blank=True, editable=False, max_length=1000, null=True)),
                ('tip_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('city', models.TextField(default='input address', editable=False)),
                ('instagram', models.CharField(blank=True, max_length=1000, null=True)),
                ('tiktok', models.CharField(blank=True, max_length=1000, null=True)),
                ('twitter', models.CharField(blank=True, max_length=1000, null=True)),
                ('youtube', models.CharField(blank=True, max_length=1000, null=True)),
                ('facebook', models.CharField(blank=True, max_length=1000, null=True)),
                ('mail', models.CharField(blank=True, editable=False, max_length=1000, null=True)),
                ('branch_code', models.CharField(default='0', editable=False, max_length=12, null=True)),
                ('branch_name', models.CharField(max_length=1000, null=True)),
                ('branch_location', models.CharField(default='Oye Ekiti', max_length=1000, null=True)),
                ('social_links', models.CharField(editable=False, max_length=1000, null=True)),
                ('links', models.CharField(editable=False, max_length=1000, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='branch account')),
            ],
            options={
                'verbose_name': 'Branch Profile',
                'verbose_name_plural': 'Branch Profiles',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('branch_name', models.CharField(editable=False, max_length=1000, null=True)),
                ('branch_location', models.CharField(editable=False, max_length=1000, null=True)),
                ('description', models.CharField(editable=False, max_length=200, null=True)),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date made')),
                ('reference', models.CharField(max_length=1000, null=True)),
                ('is_branch', models.BooleanField(default=False)),
                ('add', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.dragprofile')),
                ('payer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(related_name='user_followers', related_query_name='user_follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(related_name='followed_users', related_query_name='followed_user', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
