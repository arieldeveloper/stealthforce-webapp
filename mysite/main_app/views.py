from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
#Home page
@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        return render(request, 'main_app/index.html', {'user':request.user})
    return render(request, 'main_app/index.html')