from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phoneNumber = models.IntegerField()
    profile_image = models.ImageField(upload_to="profile/", null=True, blank=True)
    specialization = models.TextField(null=True, blank=True)
    certification = models.FileField(upload_to="Certification", null=True, blank=True)
    is_preacher = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

CHANNEL_TYPE = [
    ('IE', 'Islamic Economical System'),
    ('SO', 'Islamic Social System'),
    ('IF', 'Islamic Fatwah'),
]


class ChannelModel(models.Model):
    User = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Type = models.CharField(max_length=100, choices=CHANNEL_TYPE, default="Islamic Economical System")
    Thumbnail = models.ImageField(upload_to="Channels/Thumbnail", null=True, blank=True)
    banner = models.ImageField(upload_to="Channels/Thumbnail", null=True, blank=True)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Name)


class Subscription(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.channel) + " Subscribed by " + str(self.user)


class VideoCategoryModel(models.Model):
    type = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self) -> str:
        return str(self.type)


from django.core.exceptions import ValidationError
def file_size(value): # add this to some file where you can import it from
    limit = 300 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 300 MiB.')


class VideoModel(models.Model):
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    videoCategory = models.ForeignKey(VideoCategoryModel, on_delete=models.DO_NOTHING)
    videoFile = models.FileField(upload_to="Videos", validators=[file_size])
    videoThumbnail = models.ImageField(upload_to="Videos/thumbnails", null=True, blank=True)
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    uploaded_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Title)

class View(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    is_view = models.BooleanField(default=True)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE,related_name='view')

    def __str__(self):
        return str(self.user) + " on Video " + str(self.video)

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    is_liked = models.BooleanField(default=False)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.user) + " on Video " + str(self.video)

class Dislike(models.Model):
    id = models.AutoField(primary_key=True)
    is_disliked = models.BooleanField(default=False)
    video = models.ForeignKey(VideoModel,on_delete=models.CASCADE,related_name='dislike')
    user = models.ForeignKey(UserModel ,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.user) + " on Video " + str(self.video)

class CommentsModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    commented_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.user) + " on Video " + str(self.video)