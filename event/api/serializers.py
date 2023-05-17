from rest_framework import serializers
from user.models import DragProfile, FollowManager, Transaction
from django.utils.translation import gettext_lazy as _
import json
from event.models import DragEvent, City
from user.models import User
from django.conf import settings
from .utils import do_number
from datetime import datetime as dt




class CreateDragEventSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='user.id')
    banner = serializers.ImageField(required=False)
    class Meta:
        model= DragEvent
        fields = ['banner', 'owner_id']

    def save(self,user,info:dict):
        new_event= DragEvent(
            performer = user,
            banner = self.validated_data['banner']
        )

        new_event.title = info.get('eventTitle')
        new_event.details = info.get('eventDetail')
        new_event.city = info.get('city')
        links = info.get('links')
        new_event.direction = links[0]['link'] or ''
        new_event.website = links[1]['link'] or ''
        hosts = info.get('selectedHosts')
        new_event.links = json.dumps(links)
        new_event.hosts = json.dumps([host['id'] for host in hosts])
        new_event.venue = info.get('eventAddress')
        new_event.event_date = info.get('eventDate')
        new_event.event_time = info.get('eventTime')
        new_event.raw_date = info.get('rawDate')

        print(info.get('eventTime'))

        new_event.save()

        print(new_event.raw_date)

        return new_event

    def update(self,event,info:dict):
        new_event= DragEvent.objects.get(pk= event)

        new_event.banner = self.validated_data['banner']
        new_event.title = info.get('eventTitle')
        new_event.details = info.get('eventDetail')
        new_event.city = info.get('city')
        links = info.get('links')
        new_event.direction = links[0]['link'] or ''
        new_event.website = links[1]['link'] or ''
        hosts = info.get('selectedHosts')
        new_event.links = json.dumps(links)
        new_event.hosts = json.dumps([host['id'] for host in hosts])
        new_event.venue = info.get('eventAddress')
        new_event.event_date = info.get('eventDate')
        new_event.event_time = info.get('eventTime')
        new_event.raw_date = info.get('rawDate')

        print(info.get('eventTime'))

        new_event.save()

        print('DATE : ',info.get('rawDate'))

        return new_event

class SerializeAllEvents(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    performer_info = serializers.SerializerMethodField()
    my_links = serializers.SerializerMethodField()
    raw_date = serializers.SerializerMethodField()

    def get_raw_date(self, obj):
        return obj.raw_date

    def get_my_links(self, obj):
        return json.loads(obj.links)

    def get_banner(self, obj):
        return settings.MY_SITE + obj.banner.url

    def get_performer_info(self, obj):
        my_info =dict(
            fullname = obj.performer.fullname,
            username = obj.performer.username,
            email = obj.performer.email,

        )
        return my_info

    class Meta:
        model= DragEvent
        fields = ('id', 'raw_date','event_date','event_time','banner','title','details','venue','direction','website','my_links', 'city', 'hosts', 'performer_info')


class EventHostSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    about_me = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    tip_url = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    branch_location = serializers.SerializerMethodField()


    def get_image(self, obj):
        return settings.MY_SITE + obj.dragprofile.image.url
    
    def get_city(self, obj):
        return obj.dragprofile.city
    
    def get_followers(self, obj):
        f_manager = FollowManager.objects.get(owner=obj)
        return f_manager.count_followers()-1
    
    def get_following(self, obj):
        f_manager = FollowManager.objects.get(owner=obj.pk)
        return f_manager.count_following()-1
    
    def get_availability(self, obj):
        return obj.dragprofile.availability
    
    def get_about_me(self, obj):
        return obj.dragprofile.about_me
    
    def get_website_url(self, obj):
        return obj.dragprofile.website_url
    
    def get_tip_url(self, obj):
        return obj.dragprofile.tip_url
    
    def get_socials(self, obj):
        return json.loads('[]')
    
    def get_event(self, obj):
        return DragEvent.objects.filter(performer=obj).count()
    
    def get_branch_name(self, obj):
        return obj.dragprofile.branch_name
    
    def get_branch_location(self, obj):
        return obj.dragprofile.branch_location
    
    class Meta:
        model = User
        fields = ('id','username', 'branch_name', 'branch_location','email','tip_url', 'website_url','about_me','availability','fullname', 'city', 'image', 'followers', 'following', 'event', 'socials')


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    payer_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    add = serializers.SerializerMethodField()

    def get_date(self, obj):
        return str(obj.date_uploaded.date())
    
    def get_time(self, obj):
        time = obj.date_uploaded.time()
        print("TIME: ",time)
        if time.hour > 0 and time.hour < 12:
            comp = " am"
        else:
            comp = " pm"
        minit = str(time.minute)
        hrs = str(time.hour)
        if time.minute < 10:
            minit="0"+minit
        if time.hour < 10:
            hrs = "0"+hrs

        return '' + hrs + ":" + minit +comp


    def get_payer_name(self, obj):
        if obj.is_branch:
            return obj.payer.fullname
        else:
            return obj.description

    def get_branch_name(self, obj):
        if obj.is_branch and obj.branch:
            return obj.branch.branch_name
        else:
            return "SELF FUNDING"
    
    def get_amount(self, obj):
        ref_am = str(float(obj.amount))
        div_am = ref_am.split(".")
        if len(div_am[1])<2:
            ref_am+='0'
        if obj.add:
            if obj.is_branch:
                return "-₦"+ref_am
            return "+₦"+ref_am
        else:
            if obj.is_branch:
                return "+₦"+ref_am
            return "-₦"+ref_am

    def get_add(self, obj):
        if obj.is_branch:
            return not obj.add
        else:
            return obj.add
    
    class Meta:
        model = Transaction
        fields = ("id","amount", "time", "date", "payer_name", "branch_name", "add")

class CitySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    performer_count = serializers.SerializerMethodField()
    events_hosted_count = serializers.SerializerMethodField()
    upcoming_events_count = serializers.SerializerMethodField()

    def get_value(self, obj):
        return obj.name
    
    def get_performer_count(self, obj):
        count = DragProfile.objects.filter(city = obj.name).count() 
        return do_number(count)
    
    def get_events_hosted_count(self, obj):
        current_time = self.context['request'].GET.get('c')
        if current_time:
            query = DragEvent.objects.filter(city = obj.name)
            count = query.filter(raw_date__lt=current_time).count() 
            return do_number(count)
        else:
            return 0
    
    def get_upcoming_events_count(self, obj):
        current_time = self.context['request'].GET.get('c')
        if current_time:
            query = DragEvent.objects.filter(city = obj.name)
            count = query.filter(raw_date__gte=current_time).count()
            return do_number(count)
        else:
            return 0
    

    class Meta:
        model = City
        fields = ('key', 'value', 'events_hosted_count', 'upcoming_events_count', 'performer_count')