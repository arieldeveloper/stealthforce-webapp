from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView, CreateView)
from .models import FeedItem

# Create your views here.
class FeedListView(ListView):
    """
    Main homepage list of posts
    """
    model = FeedItem
    template_name = 'feed/feed.html'
    context_object_name = 'feed_posts' #overrides the default variable used in the html template
    ordering = ['-created_time'] #order by models created_time

class FeedItemDetailView(DetailView):
    """
    A detailed view of the item (user post) from the feed
    """
    model = FeedItem

class ItemCreateView(CreateView):
    model = FeedItem
    template_name = 'create-item.html'
    fields = ['caption']


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form) #must run the method
