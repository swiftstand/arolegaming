import base64
import json
import re
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from event.models import DragEvent
from user.models import User
from event.api.serializers import CreateDragEventSerializer, SerializeAllEvents
from random import choice
from string import ascii_letters
import itertools
from django.conf import settings
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers 
from .pagination import CustomPagination
from rest_framework import serializers






class DragEventViewSet(viewsets.ModelViewSet):
    queryset = DragEvent.objects.all()
    pagination_class = CustomPagination
    serializer_class = CreateDragEventSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


    @action(detail=False,  methods=["POST"], permission_classes=[IsAuthenticated])
    def handle_events(self, serializer):
        if self.request.method == "POST":
            print('HERE')
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})

    @action(detail=False,  methods=["GET, PUT"], permission_classes=[IsAuthenticated])
    def edit_event(self, pk=None):
        if pk:
            print('EDIT')
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def event_detail(self, pk=None):
        if pk:
            print('EDIT')
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})

    @action(detail=False,  methods=["DELETE"], permission_classes=[IsAuthenticated])
    def event_delete(self, pk=None):
        if pk:
            print('EDIT')
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})


    # @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    # def profile_event(self,):
    #         username = json.loads(self.request.data.get('user'))
    #         events = DragEvent.objects.filter(performer=username)
            

    #         event_list = []
    #         for event in events:
    #             event_dict = dict(
    #                    banner = settings.MY_SITE + event.banner.url,
    #                    title = event.title,
    #                    detail = event.details,
    #                    venue = event.venue,
    #                    website = event.website,
    #                    direction = event.direction,
    #                    performer = [event.performer.username, event.performer.fullname],
    #                    city = event.city 
    #             )

    #             event_list.append(event_dict)
    #         return Response({'status':'success'})


class ListEventViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = SerializeAllEvents
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return DragEvent.objects.all().order_by('-date_uploaded')
        # return event_query

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def profile_event(self, serializer):
        query = self.get_queryset()
        # owner=self.request.content_params['user']
        owner = 'tara_hoot'
        print(self.request.GET.get('q', None))
        # owner = self.request.data.get('user')
        if owner:
            user = User.objects.get(username=owner)
            query = query.filter(performer=user)
            serializer = self.serializer_class(query,many=True)
            result= json.loads(json.dumps(serializer.data))
    
            print(self.paginate_queryset(result))
            return Response(self.paginate_queryset(result))

