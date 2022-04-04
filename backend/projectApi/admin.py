from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserModel)
admin.site.register(VideoModel)
admin.site.register(CommentsModel)
admin.site.register(PreacherAccount)
admin.site.register(CommonUserAccount)
admin.site.register(ChannelModel)
admin.site.register(VideoCategoryModel)
admin.site.register(Dislike)
admin.site.register(Like)
admin.site.register(View)
admin.site.register(Subscription)