from django.core.serializers import serialize
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile , NetworkEdge
from rest_framework import serializers

class UserCreatedSerializer(ModelSerializer):

 def create(self,validate_data):
    validate_data['password']=make_password(validate_data['password'])
    user=User.objects.create(**validate_data)

    UserProfile.objects.create(user=user)

    return user

 class Meta:
        model=User
        fields=('username','password','email')

        #include , exclude , fields
class UserProfileViewSerializer(ModelSerializer):

    user = UserCreatedSerializer()
    class Meta:
        model=UserProfile
        fields=('bio','profile_pic_url','user_id','user')
        #exclude=('profile_pic_url', )

class UserProfileUpdateSerializer(ModelSerializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()

    def update(self,instance,validated_data):
       # user_data = validated_data.pop('user', {})
       user=instance.user
       user.first_name=validated_data.pop('first_name')
       user.last_name=validated_data.pop('last_name')
       user.save()
       instance.bio=validated_data.get("bio", None)
       instance.profile_pic_url= validated_data.get('profile_pic_url',None)
       instance.save()

       return instance

    class Meta:
        model=UserProfile
        fields=('first_name','last_name','bio','profile_pic_url')

class NetworkEdgeCreationSerializer(ModelSerializer):
      to_user=UserProfileViewSerializer()
      from_user=UserProfileViewSerializer()

      class Meta:
        model=NetworkEdge
        fields=('from_user','to_user')

class NetworkEdgeViewSerializer(ModelSerializer):
    to_user=UserProfileViewSerializer()
    from_user=UserProfileViewSerializer()
    class Meta:
        model=NetworkEdge
        fields=('from_user','to_user')