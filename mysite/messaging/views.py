from django.shortcuts import render

# Create your views here.
def inbox_view(request):
    #Show all messages
    return render(request, 'messaging/messages-view.html')

def start_direct_message(request):
    messages = {
        'test12':"hey bro",
        'arieldeveloper':"whats up man?",
        "test12":"not much, how about you",
    }
    return render(request, 'messaging/start-direct-message.html', {'messages':messages})