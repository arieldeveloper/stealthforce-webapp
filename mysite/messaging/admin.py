from django.contrib import admin
from messaging.models import Message, Conversation

# Register your models here.
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'time_sent')


admin.site.register(Message, MessagesAdmin)
admin.site.register(Conversation)