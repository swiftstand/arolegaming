import base64
import json
import re
import random
from django.http import QueryDict
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from user.models import User, DragProfile, FollowManager, Transaction
from user.api.serializers import RegistrationSerializer,LoginSerializer, CreateDragProfileSerializer
from random import choice, shuffle
from string import ascii_letters
import itertools
from operator import itemgetter
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers 
from django.core.files.uploadedfile import SimpleUploadedFile
from event.models import City, DragEvent, Bookmark
from event.api.pagination import ProfilePagination
from event.api.serializers import CitySerializer, EventHostSerializer, TransactionSerializer
from django.db import models
from decimal import Decimal
from event.api.utils import do_number
from datetime import timedelta, datetime


@api_view(['POST'])
def login(request):
    data={}
    props = request.data
    try:
        user_obj = User.objects.get(email = request.data['email'])
        # create bookmarker
        user_bookmark = Bookmark.objects.filter(owner=user_obj).exists()
        if user_bookmark == False:
            new_bookmark = Bookmark.objects.create(owner = user_obj)

        user_follow_manager = FollowManager.objects.filter(owner=user_obj).exists()
        if user_follow_manager == False:
            # create manager
            new_manager = FollowManager.objects.create(owner=user_obj)
            new_manager.followers.add(user_obj)
            new_manager.following.add(user_obj)
            new_manager.save()

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
        # create bookmarker
        user_bookmark = Bookmark.objects.create(owner=user)
        # create manager
        new_manager = FollowManager.objects.create(owner=user)
        new_manager.followers.add(user)
        new_manager.following.add(user)
        new_manager.save()

        token, created = Token.objects.get_or_create(user=user)
        data['satus']= 'success'
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
    token = request.data['tok']
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
            d_token = Token.objects.get(user=user).key
            print(user.pk, request.user.pk)
            if d_token == token and len(argue) >= 4 :
                data['msg'] = None
                data['valid'] = True
            elif len(argue)<4:
                data['msg'] = "stage name should be 4 or more characters"
                data['valid'] = False
            else:
                data['msg'] = "A user with that stage name already exists"
                data['valid'] = False
        else:
            if len(argue) >= 4:
                data['msg'] = None
                data['valid'] = True
            else:
                data['msg'] = "stage name should be 4 or more characters"
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
    follower = FollowManager.objects.get(owner=user)

    number_of_followers = follower.count_followers()

    following = follower.count_following()
    d_events = DragEvent.objects.filter(performer__in = follower.following.all())
    try:
        profile = DragProfile.objects.get(owner=user)
        all_trans = Transaction.objects.filter(branch=profile)
        end_date = datetime.now()
        end_date = str(end_date.date())
        end_date = datetime.fromisoformat(end_date)
        today_trans = all_trans.filter(date_uploaded__gte = end_date).count()
        
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
            events = DragEvent.objects.filter(performer=user).count(),
            bookmarks = Bookmark.objects.get(owner=user).bookmarked_events.all().count(),
            followed_events = d_events.count(),
            branch_code = profile.branch_code,
            all_trans= all_trans.count(),
            today_trans = today_trans
        )
    except:
        
        data = dict(
            status=True,
            username = user.username,
            fullname = user.fullname,
            followers = number_of_followers-1,
            following = following-1,
            bookmarks = Bookmark.objects.get(owner=user).bookmarked_events.all().count(),
            followed_events = d_events.count(),
            trans_numb = do_number(Transaction.objects.filter(payer=user).count()),
            balance = user.balance,
            email = user.email,
            qid = user.qr_id
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


def generate_code():
    size = random.randint(10, 15)
    result = ''.join(random.choices("123456789", k=size))
    for  i in itertools.count(1):
        if result not in User.objects.filter(qr_id=result).values_list('qr_id',flat=True):
            break
        generate_code()

    return result

class AroleViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    pagination_class = ProfilePagination
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)

    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def transactions(self, serializer):
        filterer = self.request.GET.get('f', None)
        owner = self.request.GET.get('m', None)
        if owner:
            branch = DragProfile.objects.get(owner=self.request.user)
            transactions = Transaction.objects.filter(branch=branch).order_by("-date_uploaded")    
        else:
            transactions = Transaction.objects.filter(payer=self.request.user).order_by("-date_uploaded")
        if filterer:
            end_date = datetime.now()
            end_date = str(end_date.date())
            end_date = datetime.fromisoformat(end_date)
            transactions = transactions.filter(date_uploaded__gte = end_date)
        transactions_serializer = TransactionSerializer(transactions, many=True)
        transactions_result = json.loads(json.dumps(transactions_serializer.data))

        final_result = []
        for each_day, transactions_group_by_date in itertools.groupby(transactions_result, key=itemgetter('date')):
            date_dict = {
                "date" : each_day,
                "transactions" : list(transactions_group_by_date)
            }
            final_result.append(date_dict)

        final_result = self.paginate_queryset(final_result)
        print(final_result)
        data = {
            "status" : True,
            "result" : final_result
        }

        return Response(data)




    @action(detail=False,  methods=['POST'], permission_classes=[IsAuthenticated])
    def credit_customer(self, serializer):
        body =self.request.data
        print(body)
        mail = body["email"]

        user = User.objects.get(email=mail)

        amount = Decimal(body["amount"])
        user.balance = user.balance + amount

        new_transaction = Transaction.objects.create(payer=user,amount=amount, description= "Funded Account Via Flutterwave Gateway", reference=body["ref"], add=True)

        new_transaction.branch_name = "Self Funding"
        new_transaction.is_branch = False

        new_transaction.save()
        user.save()

        return Response({
            "status" : True,
        })


    @action(detail=False,  methods=['POST'], permission_classes=[IsAuthenticated])
    def bill_customer(self, serializer):
        body =self.request.data
        pay_code =  int(body['pay'])
        mail = body["email"]
        description = body["describe"]
        is_branch = body["is_branch"]

        user = User.objects.get(email=mail)
        if pay_code != user.pay_code:
            return Response({
                "status" : False,
                "msg" : "Invalid Payment Code"
            })

        else:
            amount = Decimal(body["amount"])
            if user.balance < amount:
                return Response({
                "status" : False,
                "msg" : "Customer balance not enough"
            })
            user.balance = user.balance - amount

            new_transaction = Transaction.objects.create(payer=user,amount=amount, description= description, reference=generate_code(), add=False)

            if is_branch:
                branch_code = body["branch_code"]
                branch = DragProfile.objects.get(branch_code=branch_code)
                new_transaction.branch = branch
                new_transaction.branch_name = branch.branch_name
                new_transaction.branch_location = branch.branch_location
                new_transaction.is_branch = True
            
            else:
                new_transaction.branch_name = "Self Funding"
                new_transaction.is_branch = False

            new_transaction.save()
            user.save()

            return Response({
                "status" : True,
            })


    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def scan_qr(self, serializer): 
        try:
            code = self.request.GET.get('g', None)
            for i in User.objects.all():
                print(i.qr_id)
            print(code, User.objects.filter(qr_id = code))
            user = User.objects.get(qr_id = code)
            data = dict(
                status = True,
                name = user.fullname,
                user_name = user.email
            )
        except:
            data = {
                "status" : False
            }


        return Response(data)

    @action(detail=False,  methods=['POST'], permission_classes=[IsAuthenticated])
    def save_qr(self, serializer):
        body =self.request.data
        code = body["code"]
        pay =  body["pay"]
        user = User.objects.get(pk = self.request.user.pk)
        user.qr_id = code
        user.pay_code = pay
        user.save()
        print("NEW : ", user.qr_id)

        data = {
            "status" : True,
        }

        return Response(data)
        


    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def run_qr(self, serializer):
        print("EUN CODE : ",self.request.user.qr_id)
        if self.request.user.qr_id:
            data = dict(
                exists = True,
                new_code = generate_code(),
                code = self.request.user.qr_id
            )
        else:
            print("Now")
            data = dict(
                exists = False,
                code = generate_code(),
            )
        print("DATA : ", data)
        return Response(data)

    # @action(detail=False,  methods=['POST'], permission_classes=[IsAuthenticated])
    # def new_qr(self, serializer):
    #     info = json.loads(self.request.data.get('data'))
    #     user = User.objects.get(pk=self.request.user.pk)
    #     user.qr_id = info["code"]
    #     user.pay_code = info["pay"]
    #     user.save()

    #     return Response({"status": "success"})

class DragProfileViewSet(viewsets.ModelViewSet):
    queryset = DragProfile.objects.all()
    serializer_class = CreateDragProfileSerializer
    pagination_class = ProfilePagination
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,parsers.JSONParser)
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # profiles =  
        return User.objects.filter(is_drag_performer=True)


    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def check_created(self, serializer):
        all_cities = City.objects.all()
        city_serializer = CitySerializer(all_cities, many=True, context={'request': self.request})
        cities = json.loads(json.dumps(city_serializer.data))

        data = dict(
            already = self.request.user.is_drag_performer,
            cities = cities
        )

        return Response(data)
    

    @action(detail=False,  methods=['GET'], permission_classes=[IsAuthenticated])
    def check_following(self, serializer):
        data = {'status':False}
        user_id = self.request.GET.get('d', None)
        request_user = User.objects.get(id = self.request.user.id)

        if user_id:
            profile_user = User.objects.get(id = user_id)
            # profile_user_followers = FollowManager.objects.get(owner=profile_user).followers.all()
            request_user_followed = FollowManager.objects.get(owner=request_user).following.all()
            print(request_user_followed)
            if profile_user in request_user_followed:
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
            profile_user = User.objects.get(id = user_id)
            profile_user_followers = FollowManager.objects.get(owner=profile_user)
            request_user_followed = FollowManager.objects.get(owner=request_user)
            print("REQU : FOLL ",request_user_followed)

            value = self.request.GET.get('v')
            if value == 'follow':
                request_user_followed.following.add(profile_user)
                request_user_followed.save()
                profile_user_followers.followers.add(request_user)
                profile_user_followers.save()
                followed = True
                message = "You now follow this drag profile"

            else:
                request_user_followed.following.remove(profile_user)
                request_user_followed.save()
                profile_user_followers.followers.remove(request_user)
                profile_user_followers.save()
                followed = False
                message = "you have unfollowed this profile successfully"
            
            data = dict(
                status = True,
                message = message,
                followed = followed
            )
        else:
            data = dict(
                status = False
            )
        # print(data, user_id)
        return Response(data)


    def filter_followed(self, user_follow_manager:FollowManager):
        followed_profiles = user_follow_manager.following.all().values_list('pk', flat=True)
        return followed_profiles
    
    def filter_by_city(self, city_name):
        print(city_name)
        city_profile = DragProfile.objects.filter(city = city_name)
        city_profiles = DragProfile.objects.filter(city = city_name).values_list('owner__pk', flat=True)
        print("CITYYY : ", city_profile)
        return city_profiles
    

    @action(detail=False,  methods=['GET'])
    def all_profile(self, serializer):
        data= {}
        query= self.get_queryset()
        curr = self.request.GET.get('g', None)
        filterer = self.request.GET.get('f', None)
        owner = self.request.GET.get('t', None)
        print(filterer, owner)
        if owner:
            try:
                request_user = User.objects.get(email=owner)
                user_follow_manager = FollowManager.objects.get(owner=request_user)
                if filterer=='followed_people':
                    user_followed = self.filter_followed(user_follow_manager)
                    query = query.filter(pk__in = user_followed).exclude(pk = request_user.pk)
                
                elif filterer and 'city' in filterer.split('-'):
                    city_profiles = self.filter_by_city(filterer.split('-')[-1])
                    query = query.filter(pk__in =  city_profiles)
                profiles = list(query)
                # print(profiles)
                profile_serilizer = EventHostSerializer(profiles,many=True)
                profile_result = json.loads(json.dumps(profile_serilizer.data))

            except Exception as e:
                print(e)

                data = dict(
                    status = False,
                )
                return Response(data)
            
            
        else :
            if filterer and 'city' in filterer.split('-'):
                city_profiles = self.filter_by_city(filterer.split('-')[-1])
                query = query.filter(pk__in =  city_profiles)
            profiles = list(query)
            profile_serilizer = EventHostSerializer(profiles,many=True)
            profile_result = json.loads(json.dumps(profile_serilizer.data))

        final_result = self.paginate_queryset(profile_result)

        shuffle(final_result)
        data= {
                "status" : True,
                "result" : final_result,
            }
        
        return Response(data)

    @action(detail=False,  methods=['POST', 'GET', 'PUT'], permission_classes=[IsAuthenticated])
    def perform_create(self, serializer):
        if self.request.method == "POST":
            profile_info = json.loads(self.request.data.get('data'))
            ser = CreateDragProfileSerializer(data=self.request.data)
            if ser.is_valid():
                profile = ser.save(self.request.user, profile_info)
                return Response({'status':'success'})

        elif self.request.method == "GET":
            all_cities = City.objects.all()
            city_serializer = CitySerializer(all_cities, many=True, context={'request': self.request})
            cities = json.loads(json.dumps(city_serializer.data))
            try:
                profile = DragProfile.objects.get(owner=self.request.user)
                print(profile.city)
                data = dict(
                    status=True,
                    username = self.request.user.username,
                    image = settings.MY_SITE+profile.image.url,
                    about_me = profile.about_me,
                    city = profile.city,
                    availability = profile.availability,
                    socials = json.loads(profile.social_links),
                    links = json.loads(profile.links),
                    cities = cities
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

