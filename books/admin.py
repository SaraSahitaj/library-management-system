from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'status', 'price', 'owner', 'created_at')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'author', 'owner__username', 'owner__email')
