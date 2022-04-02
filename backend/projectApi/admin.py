from django.contrib import admin
from .models import UserModel, VideoModel, CommentsModel, PreacherAccount, CommonUserAccount, ChannelModel, VideoCategoryModel
# Register your models here.


admin.site.register(UserModel)
admin.site.register(VideoModel)
admin.site.register(CommentsModel)
admin.site.register(PreacherAccount)
admin.site.register(CommonUserAccount)
admin.site.register(ChannelModel)
admin.site.register(VideoCategoryModel)