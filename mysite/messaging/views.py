from django.shortcuts import render,  get_object_or_404, redirect
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from .forms import MessageForm
User = get_user_model() #use the custom user model instead
# Create your views here.
def inbox_view(request):
    allOthers = set()
    #Show all messages
    all_messages = Message.objects.filter(recipient=request.user) | Message.objects.filter(sender=request.user)
    for message in all_messages:
        if message.recipient == request.user:
            #messages incoming
            allOthers.add(message.sender)
        elif message.sender == request.user:
            #messages outgoing
            allOthers.add(message.recipient)
    threads = Conversation.objects.all()

    return render(request, 'messaging/inbox.html', {'all_messages':all_messages, 'threads':threads})

def conversation_view(request, pk):
    conversation = get_object_or_404(Conversation, id=pk)
    messages = Message.objects.filter(recipient=conversation.user1, sender=conversation.user2) | Message.objects.filter(recipient=conversation.user2, sender=conversation.user1)
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)  # puts all the data filled out still
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sender = conversation.user1
            obj.recipient = conversation.user2
            obj.save()

    return render(request, 'messaging/conversation.html', {'messages':messages})

def start_direct_message(request):
    return render(request, 'messaging/start-direct-message.html', {'messages':'test'})

def send_message(sender, recipient, message):
    if (Conversation.objects.filter(user1=recipient, user2=sender) | Conversation.objects.filter(user1=sender, user2=recipient)).count() > 0:
        #existing conversation exists
        Message(message=message, sender=sender, recipient=recipient)
    else:
        Message(message=message, sender=sender, recipient=recipient)
        Conversation(user1=sender, user2=recipient)

def delete_message():
    pass

