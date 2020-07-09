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
    like_count = models.PositiveIntegerField(default=0)
    # image_content = models.ImageField(upload_to='profile_pics')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.owner

    def get_absolute_url(self):
        return reverse('home')