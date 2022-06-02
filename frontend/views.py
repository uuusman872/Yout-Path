from multiprocessing import context
from operator import le
from django.http import HttpResponse
from django.shortcuts import redirect, render
from projectApi import forms
from django.contrib.auth.models import User
from django.contrib import auth
from projectApi.models import ChannelModel, CommentsModel, Dislike, Like, Subscription, UserModel, VideoModel, View
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def login_excluded(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def index(request):
    videos = VideoModel.objects.all().order_by("uploaded_date")
    context_list = []
    for vid in videos:
        views = View.objects.filter(video=vid).count()
        context_list.append({"object": vid, "views": views})
    context = {
        "context_list": context_list
    }
    return render(request, "index.html", context=context)


def videos(request):
    return render(request, "videos.html")


def channels(request):
    return render(request, "channels.html")


@login_required(login_url='login')
def videoplayer(request, pk_id):
    video = VideoModel.objects.get(id=pk_id)
    user = UserModel.objects.get(user=request.user)
    channel_name = video.channel
    form = forms.AddCommentForm()
    if Subscription.objects.filter(channel=channel_name).exists():
        subs = Subscription.objects.filter(channel=channel_name).count()
    else: 
        subs = 0

    if Subscription.objects.filter(Q(user=user) & Q(channel=channel_name)).exists():
        is_subscribed = Subscription.objects.filter(Q(user=user) & Q(channel=channel_name))[0].is_subscribed
    else:
        is_subscribed = False

    if View.objects.filter(video=video).filter(user=user).exists():
        num_views = View.objects.filter(video=video).count()

    else:
        views = View.objects.create(user=user, is_view=True, video=video)
        num_views = View.objects.filter(video=video).count()
    
    if Like.objects.filter(video=video).exists():
        like_count = Like.objects.filter(video=video).count()

    else:
        like_count = 0

    if Dislike.objects.filter(video=video).exists():
        dislike_count = Dislike.objects.filter(video=video).count()
    else:
        dislike_count = 0
    
    if CommentsModel.objects.filter(video=video).exists():
        comments = CommentsModel.objects.filter(video=video)
        num_comments = len(comments)
    else:
        num_comments = 0
        comments = []

    context = {
        "video" : video,
        "num_views": num_views,
        "channel_name":channel_name,
        "subs": subs,
        "like_count": str(like_count),
        "dislike_count": str(dislike_count),
        "num_comments": num_comments,
        "comments": comments,
        "comment_form": form,
        "is_subscribed": is_subscribed
    }
    return render(request, "videoplayer.html", context)


@login_required(login_url='login')
def LikeVideo(request, vid):
    user = UserModel.objects.get(user=request.user)
    video = VideoModel.objects.get(id=vid)

    if not Like.objects.filter(user=user, video=video).exists():
        Like.objects.create(user=user, video=video, is_liked=True)

    if Dislike.objects.filter(Q(user=user) & Q(video=video)).exists():
        dislike = Dislike.objects.filter(Q(user=user) & Q(video=video))
        dislike.delete()

    return redirect('videoplayer', vid)


@login_required(login_url='login')
def DislikeVideo(request, vid):
    user = UserModel.objects.get(user=request.user)
    video = VideoModel.objects.get(id=vid)
    if not Dislike.objects.filter(user=user, video=video).exists():
        Dislike.objects.create(user=user, video=video, is_disliked=True)

    if Like.objects.filter(Q(user=user) & Q(video=video)).exists():
        liked = Like.objects.filter(Q(user=user) & Q(video=video))
        liked.delete()
    return redirect('videoplayer', vid)



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

@login_required(login_url='login')
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

@login_required(login_url='login')
def upload_video(request):
    vform = forms.UploadVideoForm(request.POST or None, request.FILES)
    user = UserModel.objects.get(user=request.user)
    user_channel = ChannelModel.objects.filter(User=user)
    if request.method == "POST":
        if vform.is_valid():
            form = vform.save(commit=False)
            form.creator = user
            channel_name = request.POST["channel"]
            form.channel = ChannelModel.objects.filter(Q(User=user) & Q(Name=channel_name))[0]
            form.save()
            return redirect('videos')
    return render(request, "uploadVideoContent.html", context={"form":vform, "user_channel": user_channel})

@login_required(login_url='login')
def userSubscriptionView(request):
    user = UserModel.objects.get(user=request.user)
    subs = Subscription.objects.filter(user=user)
    context = {
        "subs": subs
    }
    return render(request, "UserSubscription.html", context)

@login_required(login_url='login')
def likedVideoViewList(request):
    user = UserModel.objects.get(user=request.user)
    like_videos = Like.objects.filter(user=user)
    context = {
        "like_videos": like_videos
    }
    return render(request, "likeVideosList.html", context)

@login_required(login_url='login')
def YourVideoListView(request):
    user = UserModel.objects.get(user=request.user)
    if VideoModel.objects.filter(creator=user).exists():
        user_videos = VideoModel.objects.filter(creator=user)
    else:
        user_videos = []
    context = {
        "user_videos": user_videos
    }
    return render(request, "userVideoList.html", context)


@login_required(login_url='login')
def addComment(request):
    form = forms.AddCommentForm(request.POST or None)
    user = UserModel.objects.get(user=request.user)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            id = request.POST['videoId']
            comment.video = VideoModel.objects.get(id=id)
            comment.save()
    return redirect('videoplayer', id)



def searchVideo(request):
    if request.method == "POST":
        text = request.POST["search"]
        videos_list = VideoModel.objects.filter(Q(Title__icontains=text) | Q(Description__icontains=text))
        context = {
            "video_list": videos_list
        }
        return render(request, 'searchResults.html', context)
    return redirect('badRequest.html')

def subscribeChannel(request):
    if request.method == "POST":
        c_id = request.POST['c_id']
        v_id = request.POST['v_id']
        user = UserModel.objects.get(user=request.user)
        channel = ChannelModel.objects.get(id=c_id)
        if not Subscription.objects.filter(Q(channel=channel) & Q(user=user)).exists():
            Subscription.objects.create(user=user, channel=channel, is_subscribed=True)
        return redirect('videoplayer', v_id)
    else:
        return HttpResponse("Page Not Found")


def unsubscribeChannel(request):
    if request.method == "POST":
        c_id = request.POST['c_id']
        v_id = request.POST['v_id']
        user = UserModel.objects.get(user=request.user)
        channel = ChannelModel.objects.get(id=c_id)
        if Subscription.objects.filter(Q(channel=channel) & Q(user=user)).exists():
            user = Subscription.objects.filter(Q(channel=channel) & Q(user=user))[0]
            user.delete()
        return redirect('videoplayer', v_id)
    else:
        return HttpResponse("Page Not Found")