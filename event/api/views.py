import base64
import json
import re
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from event.models import DragEvent, City
from user.models import User,DragProfile
from event.api.serializers import CreateDragEventSerializer, SerializeAllEvents, EventHostSerializer, CitySerializer
from random import choice
from string import ascii_letters
import itertools
from django.conf import settings
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers 
from .pagination import CustomPagination, ProfilePagination
from datetime import datetime
from rest_framework.authtoken.models import Token






class DragEventViewSet(viewsets.ModelViewSet):
    queryset = DragEvent.objects.all()
    pagination_class = ProfilePagination
    serializer_class = CreateDragEventSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]


    @action(detail=False,  methods=["POST"], permission_classes=[IsAuthenticated])
    def handle_events(self, serializer):
        if self.request.method == "POST":
            info = json.loads(self.request.data.get('data'))
            ser = CreateDragEventSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, info)
                return Response({'status':'success'})

    @action(detail=False,  methods=["GET"])
    def all_cities(self, pk=None):
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many =True)

        result = json.loads(json.dumps(serialized_cities.data))
        data = dict(
            result = self.paginate_queryset(result),
            status = True,
        )

        return Response(data)

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def all_event_host(self, pk=None):
        performers = DragProfile.objects.filter(approved = True).values_list('owner', flat=True)
        performers = User.objects.filter(pk__in  = performers).exclude(pk = self.request.user.pk )

        d_serializer = EventHostSerializer(performers, many=True)
        general_hosts= json.loads(json.dumps(d_serializer.data))

        # general = ,
    
        data = dict(
            result = self.paginate_queryset(general_hosts),
            status = "success",
        )
        return Response(data)


    @action(detail=False,  methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def edit_event(self, pk=None):
        if self.request.method == "GET":
            event_pk = self.request.GET.get('q', None)
            all_cities = City.objects.all()
            city_serializer = CitySerializer(all_cities, many=True)
            cities = json.loads(json.dumps(city_serializer.data))
            if int(event_pk) > 0:
                event= DragEvent.objects.get(pk = event_pk)
                event_hosts_pk = json.loads(event.hosts)
                event_hosts = User.objects.filter(pk__in = event_hosts_pk).exclude(pk = self.request.user.pk )
                d_serializer = EventHostSerializer(event_hosts, many=True)
                result= json.loads(json.dumps(d_serializer.data))
                event_serializer = SerializeAllEvents(event)
                event_obj = json.loads(json.dumps(event_serializer.data))

                
                print("CITIES\n", cities)
                data = dict(
                    hosts = result,
                    status = "success",
                    cities = cities,
                    event = event_obj
                )
                return Response(data)
            
            else:

                data = dict(
                    hosts = [],
                    status = "success",
                    cities = cities,
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


    @action(detail=False,  methods=["DELETE"],permission_classes=[IsAuthenticated])
    def event_delete(self, serializer):
        event_id = self.request.GET.get('q', None)
        # event_id = None
        if event_id:
            event = DragEvent.objects.get(pk=event_id)
            if event.performer.pk == self.request.user.pk:  
                event.delete()

                data= dict(
                    status=True,
                )

                return Response(data)
            
        data= dict(status=False)

        return Response(data)
            

    @action(detail=False,  methods=["GET"])
    def event_detail(self, serializer):
        pk =  self.request.GET.get('q', None)
        token = self.request.GET.get('t', None)
        if pk:
            try:
                event = DragEvent.objects.get(pk=pk)
                event_hosts = json.loads(event.hosts)
                host_users = User.objects.filter(id__in = event_hosts)

                creator = event.performer

                event_serialized = SerializeAllEvents(event)
                host_serializer = EventHostSerializer(host_users, many=True)
                creator_serializer = EventHostSerializer(creator)

                hosts = json.loads(json.dumps(host_serializer.data))
                performer = json.loads(json.dumps(creator_serializer.data))
                event_detail = json.loads(json.dumps(event_serialized.data))

                print("TOKEN : ", token)
                if token != 'null':
                    online = True
                else:
                    online = False
                if Token.objects.filter(user=creator).exists():
                    print("T")
                    if Token.objects.get(user=creator).key == token:
                        owner = True
                        
                    else:
                        owner = False
                else:
                    owner = False

                print(online)


                data = dict(
                    status = True,
                    creator_info=performer,
                    hosts_list = hosts,
                    owner = owner,
                    size = len(hosts),
                    event = event_detail,
                    online = online
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
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        return DragEvent.objects.all().order_by('-date_uploaded')
        # return event_query


    @action(detail=False,  methods=["GET"])
    def every_event(self, serializer):
        query= self.get_queryset()
        curr = self.request.GET.get('g', None)
        upcoming_query = query.filter(raw_date__gte=curr)
        upcoming_serializer = self.serializer_class(upcoming_query,many=True)
        upcoming_result= json.loads(json.dumps(upcoming_serializer.data))

        data= {
                "status" : True,
                "result" : self.paginate_queryset(upcoming_result),
            }
        
        return Response(data)

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def history_profile(self, serializer):
        query = self.get_queryset()
        owner = self.request.GET.get('q', None)
        curr = self.request.GET.get('g', None)

        if owner:
            try:
                user = User.objects.get(email=owner)
                history_query = query.filter(performer=user).filter(raw_date__lt=curr)
                history_serializer = self.serializer_class(history_query,many=True)
                history_result= json.loads(json.dumps(history_serializer.data))

                data= {
                    "status" : True,
                    "result" : self.paginate_queryset(history_result),
                    # "upcoming_event" :  [],
                }
            except Exception as e:
                print(e)

                data = dict(
                    status = False,
                )
            return Response(data)

    @action(detail=False,  methods=["GET"], permission_classes=[IsAuthenticated])
    def profile_event(self, serializer):
        query = self.get_queryset()
        owner = self.request.GET.get('q', None)
        curr = self.request.GET.get('g', None)
        print(curr)
        if owner:
            try:
                user = User.objects.get(email=owner)
                upcoming_query = query.filter(performer=user).filter(raw_date__gte=curr)
                upcoming_serializer = self.serializer_class(upcoming_query,many=True)
                upcoming_result= json.loads(json.dumps(upcoming_serializer.data))
                # for iq in query:
                #     print('\t',iq.raw_date, '\t', int(curr))

                # history_query = query.filter(performer=user).filter(raw_date__lt=curr)
                # history_serializer = self.serializer_class(history_query,many=True)
                # history_result= json.loads(json.dumps(history_serializer.data))

                # result_query = query.filter(performer=user)
                # result_serializer = self.serializer_class(result_query,many=True)
                # final_result= json.loads(json.dumps(result_serializer.data))
                # print(len(final_result))
                # print(self.paginate_queryset(history_result))
                print(upcoming_result)
                data= {
                    "status" : True,
                    "result" : self.paginate_queryset(upcoming_result),   
                    # "upcoming_event" :  [],
                    # "result" : self.paginate_queryset(final_result)
                }
                

            except Exception as e:
                print(e)

                data = dict(
                    status = False,
                )
            return Response(data)
        
    

