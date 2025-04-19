from http.client import responses
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import User ,UserProfile
from users.serializers import (UserCreatedSerializer , UserProfileViewSerializer,UserProfileUpdateSerializer)
from rest_framework.permissions import IsAuthenticated

def index(request):

    message = f'{request.GET["my_favourite_colour"]}'
    return HttpResponse(message)


@api_view(['POST'])
def create_user(request):
    #  user=User()
    #  user.username=request.data['username']
    #  user.first_name=request.data['first_name1']
    #  user.last_name=request.data['last_name1']
    #  user.email=request.data['email1']
    #
    #  user.save()
    #
    #  response_objects = {
    #      "email": user.email,
    #     "first_name" : user.first_name,
    #     "last_name" : user.last_name,
    #     "username" : user.username,
    #  }
    # response_data=json.loads(response_objects)

        serializer=UserCreatedSerializer(data=request.data)

        response_data = {
            "errors": None,
            "data" : None
        }

        if serializer.is_valid():

          user=serializer.save()
          refresh= RefreshToken.for_user(user)
          response_data["data"] = {
            'refresh' : str(refresh),
             'access' : str(refresh.access_token),
        }
          response_status= status.HTTP_200_OK
        else:
          response_data["errors"] =serializer.errors
          response_status= status.HTTP_400_BAD_REQUEST

        print("line -> 16", request.data)

        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    print("Request User Object -->", request.user)
    users= UserProfile.objects.all()
    serialized_data = UserProfileViewSerializer(instance=users,many=True)
    return Response(serialized_data.data ,status=status
                    .HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request , pk=None):
  user=UserProfile.objects.filter(id=pk).first()
  if user:
      serializer=UserProfileViewSerializer(instance=user)
      response_data = {
        "data": serializer.data,
        "error": None
       }
      response_status = status.HTTP_200_OK
  else:
      response_data={
          "data":None,
          "error": "User does not exist"
      }
      response_status=status.HTTP_404_NOT_FOUND

  return Response(response_data,status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_user_profile(request):
    user_profile_serializer= UserProfileUpdateSerializer(instance=request.user.profile, data=request.data)
    response_data={
        "data": None,
        "errors" : None
    }

    if user_profile_serializer.is_valid():
        user_profile=user_profile_serializer.save()
        response_data['data']=UserProfileViewSerializer(instance=user_profile).data

        response_status=status.HTTP_200_OK
    else:
        response_data['errors'] = user_profile_serializer.errors
        response_status=status.HTTP_404_NOT_FOUND

    return Response(response_data,response_status)

class UserProfileDetail(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JWTAuthentication,]

    def get(self,request):
        pass

    def post(self,request):
        pass