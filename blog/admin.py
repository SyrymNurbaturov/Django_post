from django.contrib import admin
from .models import *
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish')
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = [ 'publish']
admin.site.register(Post, PostAdmin)
class CommentAdmin(admin.ModelAdmin):
    def delete_model(self, request,obj):
        obj.delete()
    actions = [delete_model]
admin.site.register(Comment, CommentAdmin)