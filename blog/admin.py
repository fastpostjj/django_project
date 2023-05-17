from django.contrib import admin
from blog.models import Blog

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Для статей блога настраиваем список отображения.
    """
    list_display = ('title', 'slug', 'created_at', 'is_published', 'count_view')
    search_fields = ('title', 'description', 'created_at', 'is_published', 'count_view')
    list_filter = ('title', 'created_at', 'is_published', 'count_view')
    prepopulated_fields = {"slug": ("title",)}
