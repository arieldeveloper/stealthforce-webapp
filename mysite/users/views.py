from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginUserForm, ProfileEditForm#custom usercreationform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from feed.models import FeedItem
from django.contrib.auth import get_user_model
from messaging.models import Conversation
from django.db.models import Q
User = get_user_model() #use the custom user model instead

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST) #puts all the data filled out still
            if form.is_valid():
                form.save()
                messages.success(request, "You have created a new account")
                return redirect('login')
        return render(request, "users/register.html", {'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = LoginUserForm()
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is Incorrect')
        return render(request, "users/login.html", {'form':form})

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required(login_url='login')
def account_edit_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid:
            #Check if they made changes to the data or not
            if form.has_changed():
                try:
                    form.save()
                    return redirect('profile')
                except:
                    pass #displays the standard message from django
            else:
                messages.error(request, 'You have not made any changes.')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/account-edit.html", {'form':form, 'user':request.user})

def user_profile_view(request, username):
    user_being_viewed = get_object_or_404(User, username=username)
    posts = FeedItem.objects.filter(owner=user_being_viewed)

    if 'follow' in request.POST or 'unfollow' in request.POST:
        follow_or_unfollow(user_being_viewed, request.user)
    elif 'message' in request.POST:
        conversation, created = Conversation.objects.get_or_create(user1=request.user, user2=user_being_viewed)
        if created:
            #conversation already exists
            conversation = Conversation.objects.filter(Q(user1=request.user, user2=user_being_viewed) | Q(user1=user_being_viewed, user2=request.user))
        redirectUrl = '/direct/t/' + str(conversation.id)
        return HttpResponseRedirect(redirectUrl)

    context = {
        'request_user': request.user,
        'user_viewed': user_being_viewed,
        'user_posts': posts,
    }
    return render(request, "users/profile.html", context)

def followers_view(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()

    if request.method == "POST":
        the_user = User.objects.get(email=request.POST.get('hidden_input'))
        follow_or_unfollow(the_user, request.user)

    return render(request, "users/followers.html", {'user':user, 'user_followers':followers})


def following_view(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    if request.method == "POST":
        the_user = User.objects.get(email=request.POST.get('hidden_input'))
        follow_or_unfollow(the_user, request.user)

    return render(request, "users/following.html", {'user':user, 'users_following':following})

def follow_or_unfollow(userBeingFollowed, follower):
    if follower not in userBeingFollowed.followers.all():
        userBeingFollowed.followers.add(follower)
        follower.following.add(userBeingFollowed)

    elif follower in userBeingFollowed.followers.all():
        userBeingFollowed.followers.remove(follower)
        follower.following.remove(userBeingFollowed)

