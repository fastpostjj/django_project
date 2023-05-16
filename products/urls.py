from django.urls import path
# from products.views import about , index, contact, gallery,
from products.views import ProductDetailView, ProductsListView, ProductsCreateView, \
     ProductsUpdateView, ProductsDeleteView, toggle_activity_product, GetIndex, GetContact, \
    GetAbout, GetGallery, CategoryUpdateView, CategoryCreateView, CategoryDetailView, \
    CategoriesListView, CategoryDeleteView, toggle_activity_category

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    # path('index/', index, name='index'),
    path('index/', GetIndex.as_view(), name='index'),
    # path('about/', about, name='about'),
    path('about/', GetAbout.as_view(), name='about'),
    # path('gallery/', gallery, name='gallery'),
    path('gallery/', GetGallery.as_view(), name='gallery'),
    # path('contact/', contact, name='contact'),
    path('contact/', GetContact.as_view(), name='contact'),
    path('products/create/', ProductsCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductsUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductsDeleteView.as_view(), name='product_delete'),
    path('products/toggle/<int:pk>/', toggle_activity_product, name='toggle_activity_product'),

    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/toggle/<int:pk>/', toggle_activity_category, name='toggle_activity_category'),
]
