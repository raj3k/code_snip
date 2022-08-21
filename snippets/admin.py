from django.contrib import admin
from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'language', 'created']
    list_filter = ['created', 'language']


