

# Register your models here.
from django.contrib import admin
from .models import Profile, Post, Comment, Follow, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)

