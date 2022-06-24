from cgitb import text
from django import forms
from django.contrib.auth.models import User
from projectApi.models import ChannelModel, CommentsModel, UserModel, VideoModel
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
import re


def validate_password_uppercase(value):
    if not re.search(r"[A-Z]+", value):
        raise ValidationError("The password must contain at least one uppercase character.")
    else:
        return value
        
def validate_password_lowercase(value):
    if not re.search(r"[a-z]+", value):
        raise ValidationError("The password must contain at least one lower character.")
    else:
        return value

def validate_password_special(value):
    if not re.search(r"[*@!#%&()^~{}]+", value):
        raise ValidationError("The password must contain at least one special character.")
    else:
        return value

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password, validate_password_uppercase, validate_password_lowercase, validate_password_special])
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

    def __init__(self, *args, **kwargs):
        super(CreatePreacherAccountForm, self).__init__(*args, **kwargs)
        self.fields['phoneNumber'].widget.attrs['required'] = 'true'
        self.fields['specialization'].widget.attrs['required'] = 'true'
        self.fields['certification'].widget.attrs['required'] = 'true'


class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = ChannelModel
        fields = ["Name", "Type", "Thumbnail", "banner", "about"]


class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ["videoCategory", "videoFile", "videoThumbnail", "Title", "Description"]

    def __init__(self, *args, **kwargs):
        super(UploadVideoForm, self).__init__(*args, **kwargs)
        self.fields['videoThumbnail'].widget.attrs['required'] = 'true'


class AddCommentForm(forms.ModelForm):
    text= forms.CharField(label='', max_length=100 , widget=forms.TextInput(attrs={'class': "comment-textinput", 'placeholder' : "Add a Comment"}))
    class Meta:
        model = CommentsModel
        fields = ["text"]

