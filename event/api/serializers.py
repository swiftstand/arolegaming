from rest_framework import serializers
from user.models import DragProfile
from django.utils.translation import gettext_lazy as _
import json
from event.models import DragEvent
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
        fields = ('id', 'raw_date','event_date','event_time','banner','title','details','venue','website','my_links', 'city', 'hosts', 'performer_info')


class EventHostSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return settings.MY_SITE + obj.dragprofile.image.url
    
    def get_city(self, obj):
        return obj.dragprofile.city
    class Meta:
        model = User
        fields = ('id','username', 'fullname', 'city', 'image')

    
    