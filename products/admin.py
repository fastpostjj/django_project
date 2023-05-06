from django.contrib import admin
from products.models import Category, Products

# Register your models here.
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Для категорий выводится id и наименование в список отображения.
    """
    list_display = ('id', 'name',)
    list_filter = ('name',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Для продуктов выводится  id, название, цена и категория.
    Результат отображения фильтруется по категории, а также осуществляется
     поиск по названию и полю описания.
    """
    list_display = ('id', 'name', 'price','category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)