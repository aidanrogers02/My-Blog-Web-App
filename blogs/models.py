from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    """A Blog Post with a title, text, and date added"""
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        """Return a string representation of the model"""
        if len(self.title) > 50:
            return f"{self.title[:50]}..."
        else:
            return f"{self.title}"

class Comment(models.Model):
    """Comment for a particular Blog Post"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        """Return a string representation of the model"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"

class FollowersCount(models.Model):
    follower = models.CharField(max_length=1000)
    user = models.CharField(max_length=1000)

    def __str__(self):
        return self.user