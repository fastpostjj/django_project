from django.urls import path
from products.views import products_views, index

app_name = 'products'

urlpatterns = [
    path('', products_views, name='products'),
    path('index/', index, name='index'),
    ]