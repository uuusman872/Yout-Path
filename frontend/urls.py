from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from frontend import views

urlpatterns = [

    path('', views.index, name="home"),
    path('videos', views.videos, name="videos"),
    path("channels", views.channels, name="channels"),
    path('videoplayer', views.videoplayer, name="videoplayer"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile")
  
]