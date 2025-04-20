from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#
# class User(models.Model):
#     name =models.CharField(max_length=255, null=False)
#     email =models.EmailField(max_length=255,null=False,unique=True)
#     phone_number=models.CharField(max_length=10,unique=True)
#     is_active =models.BooleanField(default=False)
#     created_on =models.DateTimeField(auto_now_add=True)
#     updated_on =models.DateTimeField(auto_now=True)
#

class TimeStamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class UserProfile(TimeStamp):
    DEFAULT_PROFILE_PIC_URL="https://mywebsite.com/placeholder.png"

    #profile_pic_url= models.CharField(max_length=255,default=DEFAULT_PROFILE_PIC_URL)
    profile_pic_url=models.ImageField(upload_to='profile_pic/', blank=True)
    bio=models.CharField(max_length=255,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE, null =False, related_name='profile')

class NetworkEdge(TimeStamp):
    from_user= models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='following')
    to_user= models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='followers')

    class Meta:
        unique_together=('from_user', 'to_user',)