from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm, ProfileEditForm#custom usercreationform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
def user_profile_view(request):
    #Place to show everything under this profile
    if request.user.is_authenticated:
        pass
    return render(request, "users/profile.html")

@login_required(login_url='login')
def account_edit_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/account-edit.html", {'form':form})
