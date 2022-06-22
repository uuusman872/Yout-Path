from django.contrib import admin
from .models import *
from django.contrib.auth.models import User,Group
# Register your models here.


admin.site.register(UserModel)
admin.site.register(VideoModel)
admin.site.register(CommentsModel)
admin.site.register(ChannelModel)
admin.site.register(VideoCategoryModel)
admin.site.register(Dislike)
admin.site.register(Like)
admin.site.register(View)
admin.site.register(Subscription)


class UserWarningsForAdmin(admin.ModelAdmin):
    exclude = ['is_seen']


class GroupRemoveForAdmin(admin.ModelAdmin):
    exclude = ['_groups']


admin.site.register(UserWarning, UserWarningsForAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, GroupRemoveForAdmin)