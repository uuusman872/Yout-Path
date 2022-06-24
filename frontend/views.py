from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from projectApi import forms
from django.contrib.auth.models import User
from django.contrib import auth
from projectApi.models import ChannelModel, CommentsModel, Dislike, Like, Subscription, UserModel, VideoModel, View, UserWarning
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.contrib import messages
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
    videos = VideoModel.objects.all().order_by("-uploaded_date")
    context_list = []
    warnings = ""
    if request.user.is_authenticated and UserModel.objects.filter(user=request.user).exists():
        user = UserModel.objects.get(user=request.user)
        if UserWarning.objects.filter(user=user).exists():
            warnings = UserWarning.objects.filter(user=user).order_by('-created_date')[0]
            print("[+] Warning is ", warnings.is_seen)
            if not warnings.is_seen:
                messages.error(request, warnings.message)
                warnings.is_seen = True
                warnings.save()
    else:
        warnings = ""
    for vid in videos:
        views = View.objects.filter(video=vid).count()
        context_list.append({"object": vid, "views": views})
    context = {
        "context_list": context_list,
        "warnings": warnings
    }
    return render(request, "index.html", context=context)


def videos(request):
    user = UserModel.objects.get(user=request.user)
    videos = VideoModel.objects.filter(creator=user)
    channel = VideoModel.objects.filter()
    context = {
        "videos": videos
    }
    return render(request, "videos.html", context)


def channels_ajx(request):
    user = UserModel.objects.get(user=request.user)
    channels = ChannelModel.objects.filter(User=user)
    channel_list = []
    for channel in channels:
        subscription = Subscription.objects.filter(channel=channel).count()
        channel_list.append({"channel":channel, "subscription": subscription})

    print("[+] List of channels are ", channel_list)
    context = {
        "channel_list": channel_list
    }
    return render(request, "channels.html", context)


@login_required(login_url='login')
def videoplayer(request, pk_id):
    videos = VideoModel.objects.all().order_by("uploaded_date")
    context_list = []
    for vid in videos:
        views = View.objects.filter(video=vid).count()
        context_list.append({"object": vid, "views": views})

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
        "context_list": context_list,
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
        user = User.objects.filter(username=username)
        if len(user) > 0:
            if not user[0].is_active:
                messages.error(request, "Wait For Admin Approval!")
                return redirect('login')
            else:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    request.session['is_preacher'] = UserModel.objects.get(user=user).is_preacher
                    return redirect('home')
                else:
                    messages.error(request, "Credentials not found!")
                    return redirect('login')
        else:
            messages.error(request, "Account Does Not Exist")
        
    return render(request, "accounts/login.html")


def register(request):
    user_form = forms.UserForm(request.POST or None, request.FILES)
    user_role = request.GET.get('user-role')
    if user_role == "Common":
        form = forms.CreateAccountForm(request.POST or None, request.FILES)
    elif user_role == 'Preacher':
        form = forms.CreatePreacherAccountForm(request.POST or None, request.FILES)
    
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
            if user_role == 'Preacher':
                user.is_active = False
     
            user.save()
            account_form = form.save(commit=False)
            if user_role == 'Preacher':
                account_form.is_preacher = True
                account_form.user_type = "Preacher"
            else:
                account_form.user_type = "Common User"
            account_form.user = user
            account_form.save()
            messages.success(request, "Registration Complete")
            return redirect("login")

    context = {
        "AccountForm": form,
        "user_form": user_form
    }
    return render(request, "accounts/register.html", context)


# def profile(rquest):
#     return render(rquest, "profile.html")


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
    if UserModel.objects.get(user=request.user).is_preacher:
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
                return redirect('home')
        return render(request, "uploadVideoContent.html", context={"form":vform, "user_channel": user_channel})
    else:
        messages.error(request, "No Channel Found!")
        return redirect("home")


@login_required(login_url='login')
def userSubscriptionView(request):
    user = UserModel.objects.get(user=request.user)
    subs = Subscription.objects.filter(user=user)
    context = {
        "subs": subs,
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
        videos_list = VideoModel.objects.filter(Q(Title__icontains=text) | Q(Description__icontains=text) | Q(channel__Name__icontains=text))
        Channel = ChannelModel.objects.filter(Name__icontains=text)
        subs = False
        if request.user.is_authenticated:
            if UserModel.objects.filter(user=request.user).exists():
                user = UserModel.objects.get(user=request.user)
            else:
                user = "None"
            if Subscription.objects.filter(channel__Name__icontains=text, user=user).exists():
                subs = Subscription.objects.filter(channel__Name__icontains=text, user=user)[0].is_subscribed

        context = {
            "video_list": videos_list,
            "Channel": Channel,
            "is_subscribed": subs
        }
        return render(request, 'searchResults.html', context)
    return redirect('badRequest.html')

@login_required(login_url='login')
def subscribeChannel(request):
    if request.method == "POST":
        c_id = request.POST['c_id']
        v_id = request.POST['v_id']
        print("[+] C-id ", c_id)
        print("[+] v_id ", v_id)
        user = UserModel.objects.get(user=request.user)
        channel = ChannelModel.objects.get(id=c_id)
        if not Subscription.objects.filter(Q(channel=channel) & Q(user=user)).exists():
            Subscription.objects.create(user=user, channel=channel, is_subscribed=True)
        if v_id != "":
            return redirect('videoplayer', v_id)
        else:
            return redirect('subscription-list')
    else:
        return HttpResponse("Page Not Found")


@login_required(login_url='login')
def unsubscribeChannel(request):
    if request.method == "POST":
        c_id = request.POST['c_id']
        v_id = request.POST['v_id']
        print(c_id)
        user = UserModel.objects.get(user=request.user)
        channel = ChannelModel.objects.get(id=c_id)
        if Subscription.objects.filter(Q(channel=channel) & Q(user=user)).exists():
            user = Subscription.objects.filter(Q(channel=channel) & Q(user=user))[0]
            user.delete()
        if v_id != "":
            return redirect('videoplayer', v_id)
        else:
            return redirect('subscription-list')
    else:
        return HttpResponse("Page Not Found")


@login_required(login_url='login')
def update_profile(request):
    if request.method == "POST":
        user = UserModel.objects.get(user=request.user)
        user_obj = user.user
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        user_obj.save()
        user.phoneNumber = request.POST['phoneNumber']
        profileImage = request.FILES['profileImage']
        if profileImage is not None:
            fs = FileSystemStorage()
            filename = fs.save(profileImage.name, profileImage)
            uploaded_file_url = fs.url(filename)
            user.profile_image.name = profileImage.name
        user.save()
        return redirect('home')
    userModel = UserModel.objects.get(user=request.user)
    context = {
        "userModel": userModel
    }
    return render(request, 'update_profile.html', context)


@login_required(login_url='login')
def update_password(request):
    if request.method == "POST":
        user = UserModel.objects.get(user=request.user)
        user_obj = user.user
        old_password = request.POST['old_password']
        password = request.POST['password']
        c_password = request.POST['c_password']
        is_user = auth.authenticate(username=user_obj.username, password=old_password)
        if is_user:
            if password == c_password:
                user_obj.set_password(password)
                user_obj.save()
                return redirect("login")
        else:
            return HttpResponse("User Not Found")
    return render(request, "change_password.html")


def register_selection(request):
    return render(request, "accounts/register_selection.html")


def profile(request):
    user = UserModel.objects.get(user=request.user)
    context = {
        "user" : user,
    }
    return render(request, "profile.html", context)



def logout_view(request):
    logout(request)
    return redirect("home")


def channels(request, channel_id):
    channel = ChannelModel.objects.get(id=channel_id)
    videos = VideoModel.objects.filter(channel_id=channel.id)
    
    context = {
        "channel": channel,
        "videos": videos,
        
    }
    return render(request, "channel_view.html", context)

