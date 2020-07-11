from django.shortcuts import render, redirect
from django.views.generic import (ListView,
                                  DetailView, CreateView, UpdateView, DeleteView)
from .models import FeedItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = FeedItem
    template_name = 'feed/create-item.html'
    fields = ['caption']


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form) #must run the method

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeedItem
    template_name = 'feed/update-item.html'
    fields = ['caption']

    def test_func(self):
        """
        Ensures user is logged into correct account to edit the post
        """
        item = self.get_object()
        if self.request.user == item.owner:
            return True
        return False

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form) #must run the method

class FeedItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for deleting items posted by the user
    """
    model = FeedItem
    success_url = '/'

    def test_func(self):
        """
        Ensures user is logged into correct account to delete the post
        """
        item = self.get_object()
        if self.request.user == item.owner:
            return True
        return False