from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from frontend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('videos', views.videos, name="videos"),
    path("channels", views.channels, name="channels"),
    path('videoplayer/<int:pk_id>', views.videoplayer, name="videoplayer"),
    path('login', views.login, name="login"),
    path('register/<slug:user_role>', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path("create_channel", views.createChannel, name="createChannel")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)