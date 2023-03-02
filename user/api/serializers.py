from rest_framework import serializers
from user.models import User, DragProfile
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
import json



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['fullname', 'email', 'password', 'agreement']
        extra_kwargs = {
            'password':{'write_only': True}
        }


    def validate(self, attrs):
        fullname = attrs.get('fullname')
        email = attrs.get('email')
        agreement = attrs.get('agreement')
        password = attrs.get('password')

        if email and password and fullname and agreement:
            if User.objects.filter(email=email).exists():
                msg = _('A Drag4me account with this email already exists')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('User info is not complete, please refill the form')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def save(self):
        user= User(
            email = self.validated_data['email'],
            fullname = self.validated_data['fullname'],
            agreement = self.validated_data['agreement'],
        )

        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(AuthTokenSerializer):
    email = serializers.EmailField(
        label=_("email"),
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                d_user=User.objects.get(email=email)

                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                user = authenticate(request=self.context.get('request'),
                            email=d_user.email, password=password)
            except :
                msg = _('Email or password is incorrect.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Submitted infos are invalid, check again')
            raise serializers.ValidationError(msg, code='authorization')

        if user:
            attrs['user'] = user
            return attrs
        else:
            msg = _('Email or password is incorrect.')
            raise serializers.ValidationError(msg, code='authorization')



class CreateDragProfileSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='user.id')
    image = serializers.ImageField(required=False)
    class Meta:
        model= DragProfile
        fields = ['image', 'owner_id']

    
    def set_links(self, plat,profile_info):
        for social in profile_info['socials']:
            if social['name'] == plat:
                return social['link']
        return  profile_info.get('socials').get(plat)


        

    def save(self,user, profile_info):
        profile= DragProfile(
            owner = user,
            image = self.validated_data['image']
        )

        profile.about_me = profile_info.get('about_me')
        profile.availability = profile_info.get('availability')
        links = profile_info.get('links')
        profile.links = json.dumps(links)
        profile.website_url = links[1]['link']
        profile.tip_url = links[0]['link']
        # encoded_json = json.dumps(profile_info.get('socials'))    
        profile.social_links = json.dumps(profile_info.get('socials'))
        profile.city = profile_info.get('city')
        profile.instagram = self.set_links('instagram',profile_info)
        profile.twitter = self.set_links('twitter',profile_info)
        profile.tiktok = self.set_links('tiktok',profile_info)
        profile.facebook = self.set_links('facebook',profile_info)
        profile.youtube = self.set_links('youtube',profile_info)
        profile.mail = self.set_links('mail',profile_info)
            
        profile.save()

        print(type(profile.links))

        user = User.objects.get(id=user.pk)
        user.username = profile_info.get('username')
        user.is_drag_performer = True
        user = user.save()

        return profile

    def update(self, profile_info, user ):
        profile = DragProfile.objects.get(owner=user)

        profile.about_me = profile_info.get('about_me')
        profile.image = self.validated_data['image']
        profile.availability = profile_info.get('availability')
        print(profile_info.get('links'))
        links = profile_info.get('links')
        profile.links = json.dumps(links)
        profile.website_url = links[1]['link']
        profile.tip_url = links[0]['link']
        # encoded_json = json.dumps(profile_info.get('socials'))    
        profile.social_links = json.dumps(profile_info.get('socials'))
        profile.city = profile_info.get('city')
        profile.instagram = self.set_links('instagram',profile_info)
        profile.twitter = self.set_links('twitter',profile_info)
        profile.tiktok = self.set_links('tiktok',profile_info)
        profile.facebook = self.set_links('facebook',profile_info)
        profile.youtube = self.set_links('youtube',profile_info)
        profile.mail = self.set_links('mail',profile_info)
            
        profile.save()

        user = User.objects.get(id=user.pk)
        user.username = profile_info.get('username')
        user.is_drag_performer = True
        user = user.save()

        return profile


class MyModelSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')
    creator_id = serializers.ReadOnlyField(source='creator.id')
    image_url = serializers.ImageField(required=False)


