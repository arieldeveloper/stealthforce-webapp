from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() #use the custom user model instead
# Create your models here.

#Create chat model
class Message(models.Model):
    message = models.CharField(max_length=500, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="recipient")
    time_sent = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="user2")


