from django.urls import path
from products.views import products, index, contact, gallery, about, product

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('product/<int:pk>/', product, name='product'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('contact/', contact, name='contact'),
    ]
