from .models import FeedItem
from django.forms import ModelForm
#
# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('comment_body')

class CreatePostForm(ModelForm):
    class Meta:
        model = FeedItem
        fields = ['caption', 'image']