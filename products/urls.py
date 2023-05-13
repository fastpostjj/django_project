from django.urls import path
from products.views import index, contact, about, ProductDetailView, gallery, ProductsListView, ProductsCreateView, \
    CategoryCreateView, ProductsUpdateView, ProductsDeleteView, toggle_activity

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('contact/', contact, name='contact'),
    path('products/create/', ProductsCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductsUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductsDeleteView.as_view(), name='product_delete'),
    path('products/toggle/<int:pk>/', toggle_activity, name='toggle_activity'),

    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
]
