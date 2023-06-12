from django.contrib import admin
from products.models import Category, Products, Version


# Register your models here.
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Для категорий выводится id и наименование в список отображения.
    """
    list_display = ('id', 'name', 'is_active')
    list_filter = ('name',)
    list_display_links = ('id', 'name')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Для продуктов выводится  id, название, цена и категория.
    Результат отображения фильтруется по категории, а также осуществляется
     поиск по названию и полю описания.
    """
    list_display = ('id', 'name', 'price', 'category', 'is_active', 'user', 'is_published')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description', 'is_published')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_title', 'is_active')
    list_display_links = ('id', 'product', 'version_number', 'version_title')
    list_filter = ('id', 'product', 'version_number', 'version_title')
    search_fields = ('id', 'product', 'version_number', 'version_title', 'is_active')
