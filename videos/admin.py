from django.contrib import admin
from .models import Video
from .models import Comment

class VideoAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'upload_date', 'title', 'description', 'likes', 'dislikes')
    list_editable = ('title', 'description', 'likes', 'dislikes')
    list_display_links = ('uploaded_by', 'upload_date')
    list_filter = ('upload_date', 'uploaded_by')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'video_file', 'uploaded_by')


admin.site.register(Video, VideoAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('video', 'author', 'text', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'video__title')

admin.site.register(Comment, CommentAdmin)
