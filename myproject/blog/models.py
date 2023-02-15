from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    def get_absolute_url(self):
        return reverse('blog:detail',args=[self.id])
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.post