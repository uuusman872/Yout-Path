from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    phoneNumber = models.IntegerField()



class PreacherAccount(UserModel):
    specialization = models.TextField()
    certification = models.FileField(upload_to="Certification")
    is_preacher = models.BooleanField(default=False)


class CommonUserAccount(UserModel):
    is_commonUser = models.BooleanField(default=False)


CHANNEL_TYPE = [
    ('IE', 'Islamic Economical System'),
    ('SO', 'Islamic Social System'),
    ('IF', 'Islamic Fatwah'),
]


class ChannelModel(models.Model):
    User = models.ForeignKey(PreacherAccount, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Type = models.CharField(max_length=100, choices=CHANNEL_TYPE, default="Islamic Economical System")
    Thumbnail = models.ImageField(upload_to="Channels/Thumbnail", null=True, blank=True)
    banner = models.ImageField(upload_to="Channels/Thumbnail", null=True, blank=True)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)


class VideoCategoryModel(models.Model):
    type = models.CharField(max_length=20)
    description = models.TextField()



class VideoModel(models.Model):
    creator = models.ForeignKey(PreacherAccount, on_delete=models.CASCADE)
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    videoCategory = models.ForeignKey(VideoCategoryModel, on_delete=models.DO_NOTHING)
    videoFile = models.FileField(upload_to="Videos")
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    uploaded_date = models.DateTimeField(auto_now=True)
    
class View(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    is_view = models.BooleanField(default=True)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE,related_name='view')

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    is_liked = models.BooleanField(default=False)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Dislike(models.Model):
    id = models.AutoField(primary_key=True)
    is_disliked = models.BooleanField(default=False)
    video = models.ForeignKey(VideoModel,on_delete=models.CASCADE,related_name='dislike')
    user = models.ForeignKey(UserModel ,on_delete=models.CASCADE)


class CommentsModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    commented_date = models.DateTimeField(auto_now=True)

