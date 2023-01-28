from rest_framework import serializers
from user.models import DragProfile
from django.utils.translation import gettext_lazy as _
import json
from event.models import DragEvent




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
        new_event.links = json.dumps(links)
        new_event.direction = links[0]['link']
        new_event.website = links[1]['link']
        new_event.hosts = info.get('hosts')
        new_event.venue = info.get('eventAddress')

        new_event.save()

        return new_event

class SerializeAllEvents(serializers.ModelSerializer):
    class Meta:
        model= DragEvent
        fields = ('banner','title','details','venue','website','direction','performer', 'city', )