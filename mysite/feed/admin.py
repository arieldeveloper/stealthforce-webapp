from django.contrib import admin
from feed.models import FeedItem

# Register your models here.
class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'like_count']
    search_fields = ['owner']
admin.site.register(FeedItem, FeedItemAdmin)