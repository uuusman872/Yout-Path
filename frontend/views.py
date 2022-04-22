from django import views
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html" )


def videos(request):
    return render(request, "videos.html")

def channels(request):
    return render(request, "channels.html")

def videoplayer(request):
    return render(request, "videoplayer.html")

def login(request):
    return render(request, "accounts/login.html")

def register(request):
    return render(request, "accounts/register.html")

def profile(rquest):
    return render(rquest, "profile.html")