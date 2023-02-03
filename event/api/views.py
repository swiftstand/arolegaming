import base64
import json
import re
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from event.models import DragEvent
from user.models import User,DragProfile
from event.api.serializers import CreateDragEventSerializer, SerializeAllEvents, EventHostSerializer
from random import choice
from string import ascii_letters
import itertools
from django.conf import settings
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers 
from .pagination import CustomPagination
from datetime import datetime






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
            print(info)
            # vv = info.get('rawDate')

            # print(datetime.fromtimestamp(vv/1e3))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})


    @action(detail=False,  methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def edit_event(self, pk=None):
        if self.request.method == "GET":
            performers = DragProfile.objects.filter(approved = True).values_list('owner', flat=True)
            performers = User.objects.filter(pk__in  = performers).exclude(pk = self.request.user.pk )

            d_serializer = EventHostSerializer(performers, many=True)
            general_hosts= json.loads(json.dumps(d_serializer.data))
            
            event_pk = self.request.GET.get('q', None)
            if int(event_pk) > 0:
                event= DragEvent.objects.get(pk = event_pk)
                event_hosts_pk = json.loads(event.hosts)
                event_hosts = User.objects.filter(pk__in = event_hosts_pk).exclude(pk = self.request.user.pk )
                d_serializer = EventHostSerializer(event_hosts, many=True)
                result= json.loads(json.dumps(d_serializer.data))
                event_serializer = SerializeAllEvents(event)
                event_obj = json.loads(json.dumps(event_serializer.data))

                data = dict(
                    hosts = result,
                    general = self.paginate_queryset(general_hosts),
                    status = "success",
                    event = event_obj
                )
                print(data)
                return Response(data)
            
            else:

                print(self.paginate_queryset(general_hosts))
                data = dict(
                    hosts = [],
                    general = self.paginate_queryset(general_hosts),
                    status = "success"
                )

                return Response(data)
        else:
            event_pk = self.request.data.get('id')
            print("EV : ", event_pk)
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.update(event_pk, info)
                return Response({'status':'success'})

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def event_detail(self, serializer):
        print(serializer)
        pk =  self.request.GET.get('q', None)
        if pk:
            try:
                event = DragEvent.objects.get(pk=pk)
                event_hosts = json.loads(event.hosts)
                host_users = User.objects.filter(id__in = event_hosts)
                creator = User.objects.get(pk = self.request.user.pk)

                host_serializer = EventHostSerializer(host_users, many=True)
                creator_serializer = EventHostSerializer(creator)

                hosts = json.loads(json.dumps(host_serializer.data))
                performer = json.loads(json.dumps(creator_serializer.data))

                if event.performer == self.request.user:
                    owner = True
                else:
                    owner = False

                data = dict(
                    status = True,
                    creator_info=performer,
                    hosts_list = hosts,
                    owner = owner,
                    size = len(hosts)
                )
                print("DaTA : ", data)
                return Response(data)
            except Exception as e :
                print(e)
        data =dict(
            status = False
        )
        print("DaTA : ", data)
        return Response(data)


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
        owner = self.request.GET.get('q', None)
        if owner:
            try:
                user = User.objects.get(email=owner)
                query = query.filter(performer=user)
                serializer = self.serializer_class(query,many=True)
                result= json.loads(json.dumps(serializer.data))
                data= {
                    "status" : True,
                    "result" :  self.paginate_queryset(result)
                }
                

            except Exception as e:
                print(e)

                data = dict(
                    status = False,
                )
            return Response(data)
        
    

