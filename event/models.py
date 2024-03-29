from  django.utils import  timezone
from django.db import models
from user.models import DragProfile
from django.conf import settings
# Create your models here.



class DragEvent(models.Model):
    performer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=206)
    details = models.TextField(default='', blank=True)
    venue = models.CharField(max_length=200, default='', blank=True)
    city = models.CharField(max_length=200, default='')
    links = models.CharField(max_length=2000, editable=False, default='')
    direction = models.CharField(max_length=200, default='', blank=True)
    website = models.CharField(max_length=200, default='', blank=True)
    hosts = models.CharField(max_length= 100000, null=True)
    banner = models.ImageField(upload_to='event_pics',null=True)
    raw_date = models.IntegerField(default=0)
    event_date = models.CharField(default='', max_length=1000)
    event_time = models.CharField(default='', max_length=1000)
    date_uploaded = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    date_updated = models.DateTimeField(verbose_name='date joined', auto_now=True)



    def __str__(self) -> str:
        return '{} hosted by @{}'.format(self.title, self.performer.username)
    

    class Meta:
        db_table = "z_arole_event"
    

class City(models.Model):
    name = models.CharField(max_length=500, null=True)
    key = models.IntegerField(null=True, editable=False)
    abbr = models.CharField(max_length=100, null=True)

    def __str__(self):
        return 'city of {} USA'.format(self.name)
    
    class Meta:
        verbose_name_plural = 'Cities'

    class Meta:
        db_table = "z_arole_city"
    


class Bookmark(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookmarked_events = models.ManyToManyField(DragEvent)

    def __str__(self) -> str:
        return 'Events bookmarked by {}'.format(self.owner.email)
    
    class Meta:
        db_table = "z_arole_bookmark"