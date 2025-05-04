from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']

class YouTubeForm(forms.Form):
    url = forms.URLField(label='YouTube URL')
