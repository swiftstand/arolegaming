

from django.db import models
from  django.conf import  settings
from django.utils.text import slugify
from random import choice
from string import ascii_letters
import random
import  itertools
from  django.utils import  timezone
from datetime import datetime
from  PIL import Image
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
import json
# from event.models import DragEvent


class CustomUserManager(BaseUserManager):
    """ This is the custom manager for model user class"""

    def create_user(self,email,is_admin,is_staff,is_superuser,is_tutor,password=None):
        if not email:
            raise ValueError("Users must have an Email")

        user = self.model(
                           email=self.normalize_email(email),
                           is_admin=True,
                           is_staff=True,
                           is_superuser=True
                        )

        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, email, password):
        user= self.create_user(
                                email=self.normalize_email(email),
                                is_admin=True,
                                is_staff=True,
                                is_superuser=True,
                                is_tutor=True,
                                password=password,
                               )


class User(AbstractBaseUser):
    """ Custom User inheriting from AbstractBaseUser class"""

    email = models.EmailField(error_messages={'unique': 'A user with that email already exists.'},verbose_name='email', max_length=100, unique=True)

    username = models.CharField(
                                  help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',unique=True,
                                  validators=[UnicodeUsernameValidator()], verbose_name='username', editable=True, max_length=100000
                               )

    firstname = models.CharField(blank=True,null=True,max_length=100)

    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    fullname= models.CharField(default='swift only', blank =False, null=False, max_length= 100)
    is_drag_performer=models.BooleanField(default=False)
    agreement=models.BooleanField(verbose_name="Drag4me terms and condion",default=True)
    resetter=models.CharField(null=True, editable=False, max_length=100)
    """ To change to JsonField in production """
    settings = models.CharField(max_length=1000, editable=False, null=True)
    qr_id = models.CharField(max_length=1000, null=True)
    pay_code = models.IntegerField(editable=False, default=1234, null=True, blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=100, default=0.00, editable=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "z_arole_users"

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label ):
        return True

    def generate_username(self):
        firstname=''
        for i in self.fullname:
            if i==' ':
                break
            firstname= firstname+str( i)
        value=''+ firstname + 'drag4me' + str(timezone.now().year)
        a1=str(choice(ascii_letters))
        a2=str(choice(ascii_letters))
        a3=str(choice(ascii_letters))
        username_candidate = original_username = value+a1+a2+a3
        for i in itertools.count(1):
            if username_candidate not in User.objects.filter(username=username_candidate):
                break
            username_candidate = '{}-{}'.format(original_username, i)

        self.username = username_candidate
        self.firstname= firstname

    def set_default_settings(self, user_settings=None):
        if user_settings == None:
            default_settings = [
                [{
                    "key":1,
                    "title":"Notifications For All Events",
                    "value":False
                },
                {
                    "key":2,
                    "title":"Notifications events in my city",
                    "value":True
                },
                {
                    "key":3,
                    "title":"Followed Performers Events Notifications",
                    "value":True
                }],

                [{
                    "key":1,
                    "title":"Show Me All Events",
                    "value":False
                },
                {
                    "key":2,
                    "title":"Show Me Events In My City Only",
                    "value":False
                },
                {
                    "key":3,
                    "title":"Show Me Followed Performers Events Only",
                    "value":True
                }]
                ]
        else:
            default_settings=settings
        encoded_settings = json.dumps(default_settings)
        self.settings = encoded_settings

    def decode_settings(self):
        decoded_data = json.loads(self.settings)
        return decoded_data



    def save(self,*args, **kwargs):
        if not self.pk:
            self.generate_username()
            self.set_default_settings
        super().save()

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class DragProfile(models.Model):
    owner=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="branch account")
    image=models.ImageField(upload_to='user_profile_pics',default='user_default.png', verbose_name='branch image')
    about_me=models.TextField(blank=True,null=True, default='', verbose_name="branch description")
    approved=models.BooleanField(default=False)
    locked=models.BooleanField(default=False)
    availability = models.BooleanField(default=True, editable=False)
    website_url = models.CharField(max_length=1000, null=True, blank=True, editable=False)
    tip_url = models.CharField(max_length=1000, null=True, blank=True)
    city=models.TextField(null=False, blank=False,default='input address', editable=False)
    instagram = models.CharField(max_length=1000, null=True, blank=True)
    tiktok = models.CharField(max_length=1000, null=True, blank=True)
    twitter = models.CharField(max_length=1000, null=True, blank=True)
    youtube = models.CharField(max_length=1000, null=True, blank=True)
    facebook = models.CharField(max_length=1000, null=True, blank=True)
    mail = models.CharField(max_length=1000, null=True, blank=True, editable=False)
    branch_code = models.CharField(max_length=12, null=True, default="0", editable=False)
    branch_name = models.CharField(max_length=1000, null=True)
    branch_location = models.CharField(max_length=1000, null=True, default="Oye Ekiti")
    

    """ To change to JsonField in production """
    social_links = models.CharField(max_length=1000, null=True, editable=False)
    links = models.CharField(max_length=1000, null=True, editable=False)

    def generate_code(self):
        size = random.randint(10, 15)
        result = ''.join(random.choices("123456789", k=size))
        for  i in itertools.count(1):
            if result not in User.objects.filter(qr_id=result).values_list('qr_id',flat=True):
                break
            self.generate_code()
        return result

    def save(self):
        if self.branch_code == "0" or not self.pk:
            self.branch_code = self.generate_code()
        super().save()
        user = User.objects.get(pk = self.owner.pk)
        if not user.is_drag_performer:
            user.is_drag_performer = True
            super(User, user).save()


    def __str__(self):
        return '{}'.format(self.branch_name)
    

    class Meta:
        verbose_name = "Branch Profile"
        verbose_name_plural  = "Branch Profiles"
        db_table= "z_arole_branches"

class Transaction(models.Model):
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.SET_NULL)
    branch = models.ForeignKey(DragProfile, null=True,on_delete= models.SET_NULL)
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    branch_name = models.CharField(max_length=1000, null= True, editable=False)
    branch_location = models.CharField(max_length=1000, null=True, editable=False)
    description = models.CharField(max_length=200, null=True,editable=False)
    date_uploaded = models.DateTimeField(verbose_name='date made', default=timezone.now)
    reference= models.CharField(max_length=1000, null=True)
    is_branch = models.BooleanField(default=False)
    add = models.BooleanField(default=False)
    completed = models.BooleanField(default=True)    

    def __str__(self) -> str:
        if self.add:
            return f'{self.payer.fullname} funded ₦{self.amount} via {self.description}'
        else:
            return f'{self.branch_name} Branch billed {self.payer.fullname} ₦{self.amount}'
    

    class Meta:
        db_table = "z_arole_transactions"



class FollowManager(models.Model):
    owner=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='user_followers', related_query_name='user_follower', )
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_users', related_query_name='followed_user', )

    def count_followers(self):
        followers_count = len(
            FollowManager.objects.filter(pk=self.pk).values_list('followers',flat=True))
        return followers_count

    def count_following(self):
        following_count = len(
            FollowManager.objects.filter(pk=self.pk).values_list('following',flat=True))
        return following_count

    def save(self,*args,**kwargs):
        super().save()

    def __str__(self) -> str:
        return '{} has {} followers and is following {} performers'.format(
            self.owner.username, self.count_followers()-1, self.count_following()-1
        )


    class Meta:
        db_table = "z_arole_follow_manager"