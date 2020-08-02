from django.shortcuts import render

# Create your views here.
def inbox_view(request):
    #Show all messages
    return render(request, 'messaging/messages-view.html')