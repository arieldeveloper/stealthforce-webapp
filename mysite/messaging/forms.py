from .models import Conversation, Message
from django.forms import ModelForm

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
