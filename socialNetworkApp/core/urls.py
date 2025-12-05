from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns=[
    # path('',index,name='index'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('',login_page ,name='login'),
    path('logout',logut_user ,name='logout'),
    path('profile/',Profile.as_view(),name='profile'),
    path('account-settings/',AccountSettingsView.as_view(),name='account_settings'),
    path('new-post/',CreatePost.as_view(),name='new_post'),
    
]