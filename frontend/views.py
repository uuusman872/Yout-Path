from django import views
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html" )


def playback(request):
    return render(request, "playback.html")

def videoplayer(request):
    return render(request, "videoplayer.html")