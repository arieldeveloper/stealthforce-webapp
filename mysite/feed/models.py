from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model() #use the custom user model instead
from django.urls import reverse

# Create your models here.
class FeedItem(models.Model):
    """
    Model for posts inside the feed of the homepage
    """
    caption = models.CharField(max_length=255, blank=True, null=True) #Allow user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def __unicode__(self):
        return self.owner

    @property
    def number_of_likes(self):
        return self.liked.all().count()

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
    @property
    def comment_count(self):
        return Comment.objects.filter(feedItem=self).count()
CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)
class LikeModel(models.Model):
    """
    Like model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(FeedItem, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    feedItem = models.ForeignKey(FeedItem, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=70)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
