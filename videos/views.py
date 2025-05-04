from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Comment, VideoReaction
from .forms import VideoForm, YouTubeForm
from pytube import YouTube
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseBadRequest
import logging
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required





def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    comments = video.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            Comment.objects.create(video=video, author=request.user, text=text)
            return redirect('video_detail', video_id=video.id)

    related_videos = Video.objects.exclude(id=video.id)[:5]

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
    })


def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.likes += 1
    video.save()
    return redirect('video_detail', video_id=video.id)

def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.dislikes += 1
    video.save()
    return redirect('video_detail', video_id=video.id)

def home(request):
    query = request.GET.get('q')
    videos = Video.objects.filter(title__icontains=query) if query else Video.objects.all()
    return render(request, 'videos/home.html', {'videos': videos, 'query': query})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация после регистрации
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def react_to_video(request, video_id, reaction_type):
    video = get_object_or_404(Video, id=video_id)

    if reaction_type not in ['like', 'dislike']:
        return redirect('home')

    # обновляем или создаем реакцию
    obj, created = VideoReaction.objects.update_or_create(
        user=request.user,
        video=video,
        defaults={'reaction': reaction_type}
    )

    return redirect('video_detail', video_id=video.id)


