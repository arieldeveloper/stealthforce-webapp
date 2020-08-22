from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView,
                                  DetailView, CreateView, UpdateView, DeleteView)
from .models import FeedItem, LikeModel, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
User = get_user_model() #use the custom user model instead
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import CreatePostForm
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

def feed_item_view(request, pk):
    user_post = get_object_or_404(FeedItem, id=pk)
    comments = Comment.objects.filter(feedItem=user_post)

    context = {"user_post":user_post, "comments":comments}

    if request.method == "POST":
        comment_body = request.POST.get('comment_field')
        if comment_body != "": #posted empty comment
            comment = Comment(feedItem=user_post, username=request.user.username, body=comment_body)
            comment.save()
    return render(request, "feed/feed-item.html", context)

def create_item_view(request):
    form = CreatePostForm(instance=request.user)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            item = FeedItem(owner=request.user, caption=form.cleaned_data['caption'], image=form.cleaned_data['image'])
            item.save()
            return redirect('home')
    return render(request, 'feed/create-item.html', {'form':form})


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




# class ItemCreateView(LoginRequiredMixin, CreateView):
#     model = FeedItem
#     template_name = 'feed/create-item.html'
#     fields = ['caption']
#
#     def get_success_url(self):
#         return reverse('home')
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form) #must run the method