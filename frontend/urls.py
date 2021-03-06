from django.urls import path
from frontend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('videos', views.videos, name="videos"),
    path("channels_ajx", views.channels_ajx, name="channels_ajx"),
    path('videoplayer/<int:pk_id>', views.videoplayer, name="videoplayer"),
    path('video-like/<int:vid>', views.LikeVideo, name="video-like"),
    path('video-dislike/<int:vid>', views.DislikeVideo, name="video-dislike"),
    path('add_comment', views.addComment, name='add_comment'),
    path('liked-video-list', views.likedVideoViewList, name="liked-video-list"),
    path('your_video_list_view', views.YourVideoListView, name="your_video_list_view"),
    path('subscription-list', views.userSubscriptionView, name="subscription-list"),
    path('search_video', views.searchVideo, name="search_video"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('update_profile', views.update_profile, name="update_profile"),
    path('profile', views.profile, name="profile"),
    path('update_password', views.update_password, name="update_password"),
    path("create_channel", views.createChannel, name="createChannel"),
    path("upload_video", views.upload_video, name="upload-video"),
    path("subscribe-channel", views.subscribeChannel, name="subscribe-channel"),
    path("unsubscribe-channel", views.unsubscribeChannel, name="unsubscribe-channel"),
    path("register_selection", views.register_selection, name="register_selection"),
    path("logout", views.logout_view, name="logout"),
    path("channels/<int:channel_id>", views.channels, name="channels"),
    path('comment_delete/<int:param>/<int:pk>', views.CommentDeleteView.as_view() , name="comment_delete"),
    path("update_comment/<int:param>/<int:pk>", views.UpdateCommentMessageView.as_view(), name="update_comment")
 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)