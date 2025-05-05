from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import  JWTAuthentication
from .models import UserPost
from .serializers import UserPostCreateSerializer,PostMediaCreateSerializer, PostFeedSerializer
from rest_framework import generics , mixins
# Create your views here.

class UserPostCreateFeed(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):
   permission_classes =[IsAuthenticated,]
   authentication_classes = [JWTAuthentication,]
   queryset = UserPost.objects.all()
   serializer_class = UserPostCreateSerializer

   def get_serializer_context(self):
    return {'current_user':self.request.user.profile}

   def get_serializer_class(self):
       if self.request.method == 'GET':
           return PostFeedSerializer

       return self.serializer_class

   def post(self,request,*args,**kwargs):
      return self.create(request,*args,**kwargs)

   def get(self,request,*args,**kwargs):
       return self.list(request,*args,**kwargs)
class PostMediaView(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    permission_classes =[IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]
    queryset = UserPost.objects.all()
    serializer_class = PostMediaCreateSerializer

    def put(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class UserPostDetailUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes =[IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]
    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)


