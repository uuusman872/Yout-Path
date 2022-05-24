from django.urls import path
from frontend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('videos', views.videos, name="videos"),
    path("channels", views.channels, name="channels"),
    path('videoplayer/<int:pk_id>', views.videoplayer, name="videoplayer"),
    path('video-like/<int:vid>', views.LikeVideo, name="video-like"),
    path('video-dislike/<int:vid>', views.DislikeVideo, name="video-dislike"),
    path('add_comment', views.addComment, name='add_comment'),
    path('liked-video-list', views.likedVideoViewList, name="liked-video-list"),
    path('your_video_list_view', views.YourVideoListView, name="your_video_list_view"),
    path('subscription-list', views.userSubscriptionView, name="subscription-list"),
    path('search_video', views.searchVideo, name="search_video"),
    path('login', views.login, name="login"),
    path('register/<slug:user_role>', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path("create_channel", views.createChannel, name="createChannel"),
    path("upload_video", views.upload_video, name="upload-video")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)