from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView , TokenObtainPairView, TokenObtainPairView, TokenVerifyView)

from . import views
urlpatterns = [
    path('',views.index, name="users_main_view"),
    path('add/',views.create_user , name='create_user_api'),
    path('token/refresh', TokenRefreshView.as_view(),name="token_fresh_api"),
    path('token/verify',TokenVerifyView.as_view(), name="token_verify_api"),
    path('login/api',TokenObtainPairView.as_view(),name="login_api"),
    path('list/', views.user_list, name="user_list_api"),
    path('<int:pk>/',views.get_user,name="get_single_user"),
    path('update/',views.update_user_profile, name='update_profile_api')
    path('<int:pk>/',views.UserProfileDetails.as_view(),name='user_profile_detail_api')
]
