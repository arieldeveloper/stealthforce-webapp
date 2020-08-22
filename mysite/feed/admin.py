from django.contrib import admin
from feed.models import FeedItem, LikeModel, Comment

# Register your models here.
class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'number_of_likes']
    search_fields = ['owner']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('username', 'body')

admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikeModel)