from django.shortcuts import render, redirect
from django.views.generic import (ListView,
                                  DetailView, CreateView, UpdateView, DeleteView)
from .models import FeedItem, LikeModel
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model() #use the custom user model instead
from django.http import HttpResponseRedirect

# Create your views here.
from django.contrib.auth.decorators import login_required

class feed_view(ListView):
    """
    Main homepage list of posts
    """
    model = FeedItem
    template_name = 'feed/feed.html'
    context_object_name = 'feed_posts' #all posts
    ordering = ['-created_time'] #order by models created_time

    def get_context_data(self, *args, **kwargs):
        context = super(feed_view, self).get_context_data(*args, **kwargs)
        context['user'] = self.request.user
        return context

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

def liked_by_users(request):
    # Place to show everything under this profile
    liked_by_info = False #Change this
    return render(request, "feed/liked-by-users.html")

def like_post(request):
    user = request.user
    if request.method == "POST": #if user like button pressed
        post_id = request.POST.get('post_id') #gets post id
        post_object = FeedItem.objects.get(id=post_id)

        if user in post_object.liked.all():
            post_object.liked.remove(user)
        else: #like button not clicked yet
            post_object.liked.add(user)

        #create like model
        like, created = LikeModel.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
    return HttpResponseRedirect(reverse('home'))


"""
{ % if feed_post.like_count > 1 or feed_post.like_count == 0 %}
{ % firstof
"likes" as word_likes %}
{ % endif %}
{ % if feed_post.like_count == 1 %}
{ % firstof
"like" as word_likes %}
{ % endif %}
"""