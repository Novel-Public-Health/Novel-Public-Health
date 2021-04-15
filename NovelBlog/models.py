from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    intro = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return self.title + ' |  ' + str(self.author)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_added']
        
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    def get_absolute_url(self):
        success_url = reverse_lazy('home')
        return success_url


