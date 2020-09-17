from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()  # use the custom user model instead

# Create your views here.
#Home page
@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        return render(request, 'main_app/index.html', {'user':request.user})
    return render(request, 'main_app/index.html')

def search_page_view(request, keyword=None):
    if request.method == "POST":
        search_value = request.Post.Get['search_bar']
        if search_value:
            return redirect("/search/" + str(search_value))

    user_list = User.objects.filter(username__icontains=str(keyword))
    return render(request, 'main_app/search-page.html', {'users':user_list, 'request_user':request.user})

