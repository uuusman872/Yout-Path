from enum import unique
from turtle import ondrag
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
    Like_ratio = models.IntegerField()
    Dislike_ratio = models.IntegerField()
    


class CommentsModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    commented_date = models.DateTimeField(auto_now=True)