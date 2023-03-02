from rest_framework import serializers
from user.models import DragProfile, FollowManager
from django.utils.translation import gettext_lazy as _
import json
from event.models import DragEvent, City
from user.models import User
from django.conf import settings




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
        return json.loads(obj.dragprofile.social_links)
    
    def get_event(self, obj):
        return DragEvent.objects.filter(performer=obj).count()
    class Meta:
        model = User
        fields = ('id','username', 'tip_url', 'website_url','about_me','availability','fullname', 'city', 'image', 'followers', 'following', 'event', 'socials')

class CitySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        return obj.name
    class Meta:
        model = City
        fields = ('key', 'value')