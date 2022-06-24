from django.contrib import admin

from .models import BlogPost, Comment, FollowersCount

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(FollowersCount)
