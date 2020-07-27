from django.contrib import admin
from feed.models import FeedItem, LikeModel

# Register your models here.
class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'number_of_likes']
    search_fields = ['owner']

admin.site.register(FeedItem, FeedItemAdmin)

admin.site.register(LikeModel)