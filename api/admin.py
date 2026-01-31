from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'xp', 'level', 'region', 'is_founder')
    search_fields = ('nickname',)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'author_name', 'created_at')
    list_filter = ('content_type',)

admin.site.register(EducationTheme)
admin.site.register(Event)