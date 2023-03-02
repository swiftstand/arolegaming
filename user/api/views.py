import base64
import json
import re
from django.http import QueryDict
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from user.models import User, DragProfile, FollowManager
from user.api.serializers import RegistrationSerializer,LoginSerializer, CreateDragProfileSerializer
from random import choice, shuffle
from string import ascii_letters
import itertools
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers 
from django.core.files.uploadedfile import SimpleUploadedFile
from event.models import DragEvent
from event.api.pagination import ProfilePagination
from event.api.serializers import EventHostSerializer


@api_view(['POST'])
def login(request):
    data={}
    props = request.data
    try:
        user_obj = User.objects.get(email = request.data['email'])
        props['username'] = user_obj.username
    except User.DoesNotExist:
        msg = _('Email or password is incorrect.')
        return Response({'non_field_errors': [msg]})
    serializer = LoginSerializer(data=props)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        try:
            user_token = Token.objects.get(user=user)
            """resetting token"""
            user_token.delete()
        except Token.DoesNotExist:
            """nothing"""
        token = Token.objects.create(user=user)
        data['satus']= 'success'
        data['token']= token.key
        data['fullname']= user.fullname
        data['performer'] = user_obj.is_drag_performer
        if user_obj.is_drag_performer:
            profile = DragProfile.objects.get(owner = user)
            data['approval'] = profile.approved
        else:
            data['approval'] = False
    else:
        data = serializer.errors
        data['status']='fail'

    return Response(data)


@api_view(['POST'])
def Register(request):
    data={}
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data['satus']= 'success'
        # data['image']  = user.image
        data['token']= token.key
        data['email']= user.email
        data['fullname']= user.fullname
        data['performer'] = False
        data['approval'] = False
    else:
        data = serializer.errors
        data['status']='fail'

    return Response(data)

@api_view(['POST'])
def check_unique(request):
    data = {}
    argue = request.data['argue']
    if request.data['type'] == 'mail':
        is_dere = User.objects.filter(email = argue).exists()
        if is_dere:
            user = User.objects.get(email = argue)
            if user.pk == request.user.pk:
                data['valid'] = True
            else:
                data['valid'] = False
        else:
            data['valid'] = True

    else:
        is_dere = User.objects.filter(username = argue).exists()
        if is_dere:
            user = User.objects.get(username = argue)
            print(len(argue))
            if user.pk == request.user.pk and len(argue) >= 4:
                data['valid'] = True
            else:
                data['valid'] = False
        else:
            if len(argue) >= 4:
                data['valid'] = True
            else:
                data['valid'] = False

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def Logout(request):
    data = {}
    try:
        token=Token.objects.get(user=request.user)
        token.delete()
        data['status'] = 'success'
        data['user'] = request.user.email 
    except Token.DoesNotExist:
        data['status'] = 'success'
        data['user'] = request.user.email 

    return Response(data)



def set_resetter():
    size = choice([10,11,12])
    entity=ascii_letters+'123456789'
    value=''
    for  i in itertools.count(1):
        for i in range(0,size):
            pick = str(choice(entity))
            value+=pick
        if value not in User.objects.filter(resetter=value).values_list('resetter',flat=True):
            break
        set_resetter()
    return value

@api_view(['POST'])
def forgotpassword(request):
    data = {}
    email = request.data['email']

    try:
        user=User.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.delete()
            token = Token.objects.create(user=user)
        token.save()
        reset_val=set_resetter()
        """email_subject='Hi {}, Request to Reset Password'.format(user.fullname)
        email_body='we received a request to reset your account password.If this request was not made by you kindly ignore as your account is safe with us.\nIf the request was made by you kindly make use of the code below.\n\n\n{}'.format(reset_val)
        email = EmailMessage(
                                email_subject,
                                email_body,
                                'officialswiftstand@gmail.com',
                                [user.email],
                            )
        email.send(fail_silently=False)"""
        user.resetter='123456789abc'
        user.save(update_fields=['resetter'])
        data['status'] = 'success'
        data['token'] = token.key
    except User.DoesNotExist:
        data['status'] = 'fail'
        data['info'] = 'The email provided does not exist in our system'
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def confirm_reset(request):
    data = {}
    user=request.user
    token=Token.objects.get(user=request.user)
    provided_resetter=request.data['code']
    if provided_resetter == user.resetter:
        new_password = request.data['password']
        user.set_password(new_password)
        user.resetter=''
        user.save()
        data['status']='success'
        data['token']=token.key
        data['email']=user.email
        data['fullname'] = user.fullname
    else:
        data['status']='fail'
        data['info']='The code entered is wrong, Try again!'
    
    return Response(data)

@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated,])
def request_dragprofile(request):
    data = request.data
    socials = data.pop('socials')
    

class MultipartJsonParser(parsers.MultiPartParser):
      def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )

        base64_file = result.data.get('file')
        file_parts = base64_file.split(',')
        mime_type = re.sub(r'^data:([\w\/]+);base64$', '\\1', file_parts[0])
        file = SimpleUploadedFile('file', base64.b64decode(file_parts[1]), mime_type)
        data = json.loads(result.data["data"]) or {}  # additional data sent by Expo app
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, {'file': file})


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def prepare_drag_profile(request):
    user = request.user
    profile = DragProfile.objects.get(owner=user)
    follower = FollowManager.objects.get(owner=user)

    number_of_followers = follower.count_followers()

    following = follower.count_following()
    print(number_of_followers, following)

    data = dict(
        status=True,
        username = user.username,
        fullname = user.fullname,
        image = settings.MY_SITE+profile.image.url,
        about_me = profile.about_me,
        city = profile.city,
        availability = profile.availability,
        socials = json.loads(profile.social_links),
        website_url = profile.website_url,
        tip_url = profile.tip_url,
        followers = number_of_followers-1,
        following = following-1,
        events = DragEvent.objects.filter(performer=user).count()
    )
    print("succes : ", data)   
    
    return Response(data)



@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def drag_status(request):
    user = request.user
    result={}
    if user.is_drag_performer:
        try:
            profile = DragProfile.objects.get(owner = user)
            result['approval'] = profile.approved
            result['locked'] = profile.locked
            result['performer'] = True
            result['status'] = True
        except:
            result['performer'] = False
            result['approval'] = False
    else:
        result['performer'] = False

    return Response(result)




class DragProfileViewSet(viewsets.ModelViewSet):
    queryset = DragProfile.objects.all()
    serializer_class = CreateDragProfileSerializer
    pagination_class = ProfilePagination
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # profiles =  
        return User.objects.all()


    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def check_created(self, serializer):
        data = dict(
            already = self.request.user.is_drag_performer
        )

        return Response(data)
    

    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def check_following(self, serializer):
        data = {'status':False}
        user_id = self.request.GET.get('d', None)
        request_user = User.objects.get(id = self.request.user.id)

        if user_id:
            manager = FollowManager.objects.filter(owner__id=user_id).values_list('followers',flat=True)
            if request_user.pk in manager:
                followed =True
            else:
                followed = False

            data = dict(
                status = True,
                followed = followed
            )
        return Response(data)


    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def handle_follow(self, serializer):
        data = {}
        user_id = self.request.GET.get('d', None)
        request_user = User.objects.get(id = self.request.user.id)
        if user_id:
            value = self.request.GET.get('v')
            manager = FollowManager.objects.get(owner__id=user_id)
            if value == 'follow':
                manager.followers.add(request_user)
                manager.save()
                followed = False
                message = "you have unfollowed this profile successfully"

            else:
                manager.followers.remove(request_user)
                manager.save()
                followed = True
                message = "You now follow this drag profile"
            
            data = dict(
                status = True,
                message = message,
                followed = followed
            )
        else:
            data = dict(
                status = False
            )
        print(data, user_id)
        return Response(data)
    

    @action(detail=False,  methods=['GET'])
    def all_profile(self, serializer):
        data= {}
        query= self.get_queryset()
        curr = self.request.GET.get('g', None)
        filterer = self.request.GET.get('f', None)
        print(filterer)
        if filterer == 'null':
            profiles = list(query)
            print(profiles)
            profile_serilizer = EventHostSerializer(profiles,many=True)
            profile_result = json.loads(json.dumps(profile_serilizer.data))
            print(profile_result)
            data= {
                "status" : True,
                "result" : self.paginate_queryset(profile_result),
            }
        
        return Response(data)


    @action(detail=False,  methods=['POST', 'GET', 'PUT'], permission_classes=[IsAuthenticated])
    def perform_create(self, serializer):
        if self.request.method == "POST":
            profile_info = json.loads(self.request.data.get('data'))
            ser = CreateDragProfileSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, profile_info)
                if profile:
                    try:
                        new_manager = FollowManager.objects.create(owner=self.request.user)
                        new_manager.save()
                    except:
                        non = "null"
                return Response({'status':'success'})

        elif self.request.method == "GET":
            try:
                profile = DragProfile.objects.get(owner=self.request.user)
                data = dict(
                    status=True,
                    username = self.request.user.username,
                    image = settings.MY_SITE+profile.image.url,
                    about_me = profile.about_me,
                    city = profile.city,
                    availability = profile.availability,
                    socials = json.loads(profile.social_links),
                    links = json.loads(profile.links)
                )
            except Exception as E:
                data = {
                    "status":False
                }
            
            return Response(data)

        else:
            profile_info = json.loads(self.request.data.get('data'))
            ser = CreateDragProfileSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.update(profile_info, self.request.user)

            return Response({"status" : True})

