from cgitb import text
from django import forms
from django.contrib.auth.models import User
from projectApi.models import ChannelModel, CommentsModel, UserModel, VideoModel


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["phoneNumber"]


class CreatePreacherAccountForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["phoneNumber", "specialization", "certification"]


class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = ChannelModel
        fields = ["Name", "Type", "Thumbnail", "banner", "about"]


class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ["videoCategory", "videoFile", "Title", "Description"]


class AddCommentForm(forms.ModelForm):
    text= forms.CharField(label='', max_length=100 , widget=forms.TextInput(attrs={'class': "comment-textinput", 'placeholder' : "Add a Comment"}))
    class Meta:
        model = CommentsModel
        fields = ["text"]

