from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.reactions.filter(reaction='like').count()

    def dislikes_count(self):
        return self.reactions.filter(reaction='dislike').count()


class VideoReaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍 Лайк'),
        ('dislike', '👎 Дизлайк'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    reacted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')  # 🛡️ один пользователь — одна реакция на видео

    def __str__(self):
        return f"{self.user.username} → {self.reaction} [{self.video.title}]"




class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.video.title}"



