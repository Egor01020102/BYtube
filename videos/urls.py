from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),
    path('video/<int:video_id>/react/<str:reaction_type>/', views.react_to_video, name='react_to_video'),
]

