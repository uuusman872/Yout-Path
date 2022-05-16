from multiprocessing import context
from django import views
from django.http import HttpResponse
from django.shortcuts import redirect, render
from projectApi import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import make_password

from projectApi.models import UserModel, VideoModel
# Create your views here.

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def index(request):
    videos = VideoModel.objects.all().order_by("uploaded_date")
    print(videos)
    return render(request, "index.html" )


def videos(request):
    return render(request, "videos.html")


def channels(request):
    return render(request, "channels.html")


def videoplayer(request, pk_id):
    video = VideoModel.objects.get(id=pk_id)
    context = {
        "video" : video
    }
    return render(request, "videoplayer.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, "accounts/login.html")



def register(request, user_role):
    user_form = forms.UserForm(request.POST or None)
    if user_role == "common":
        form = forms.CreateAccountForm(request.POST or None)
    elif user_role == 'preacher':
        form = forms.CreatePreacherAccountForm(request.POST or None)
    
    if request.method == 'POST':
        print("Got POST requs")
        if form.is_valid() and user_form.is_valid():
            user = User()
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.username = user_form.cleaned_data['username']
            password = user_form.cleaned_data["password"]
            user.set_password(password)
            if user_role == 'preacher':
                user.is_active = False
            user.save()
            account_form = form.save(commit=False)
            account_form.user = user
            account_form.save()
            return HttpResponse("Account Created")

    context = {
        "AccountForm": form,
        "user_form": user_form
    }
    return render(request, "accounts/register.html", context)


def profile(rquest):
    return render(rquest, "profile.html")


def uploadVideos(request):
    return render(request, "uploadVideoContent.html")


def createChannel(request):
    channelForm = forms.CreateChannelForm(request.POST or None, request.FILES)
    if request.method == "POST":
        if channelForm.is_valid():
            cform = channelForm.save(commit=False)
            user = UserModel.objects.get(user=request.user)
            cform.User = user
            cform.save()
            return redirect("home")

    return render(request, "CreateChannel.html", context={"channelForm": channelForm})