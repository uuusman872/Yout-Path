from django.contrib import admin
from .models import *
# Register your models here.


class UserModelInfo(admin.ModelAdmin):
    list_display = ("user", "full_name", "email", "phoneNumber", "user_type")

    def full_name(self, obj):
        return obj.user.first_name + obj.user.last_name

    def email(self, obj):
        return obj.user.email


admin.site.register(UserModel, UserModelInfo)
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


admin.site.register(UserWarning, UserWarningsForAdmin)