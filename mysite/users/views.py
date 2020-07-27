from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginUserForm, ProfileEditForm#custom usercreationform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from feed.models import FeedItem
from django.contrib.auth import get_user_model
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
    return render(request, "users/account-edit.html", {'form':form})

def user_profile_view(request, username):
    user_being_viewed = get_object_or_404(User, username=username)
    posts = FeedItem.objects.filter(owner=user_being_viewed)

    context = {
        'request_user': request.user,
        'user_viewed': user_being_viewed,
        'user_posts': posts,
    }
    return render(request, "users/profile.html", context)