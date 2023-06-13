from django.urls import path
# from products.views import about , index, contact, gallery,
from products.views import ProductDetailView, ProductsListView, ProductsCreateView, \
     ProductsUpdateView, ProductsDeleteView, ProductsNotPublishedView, toggle_activity_product, GetIndex, GetContact, \
    GetAbout, GetGallery, CategoryUpdateView, CategoryCreateView, CategoryDetailView, \
    CategoriesListView, CategoryDeleteView, toggle_activity_category
from products.views import VersionDetailView, VersionsListView, VersionCreateView, \
    VersionUpdateView, Toggle_Activity_Version, VersionDeleteView, VersionsDraftListView
from products.views import error

app_name = 'products'

urlpatterns = [
    path('index/', GetIndex.as_view(), name='index'),
    path('', GetAbout.as_view(), name='about'),
    path('gallery/', GetGallery.as_view(), name='gallery'),
    path('contact/', GetContact.as_view(), name='contact'),

    path('products/', ProductsListView.as_view(), name='products'),
    path('products/not_published', ProductsNotPublishedView.as_view(), name='products_not_published'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('products/create/', ProductsCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductsUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductsDeleteView.as_view(), name='product_delete'),
    path('products/toggle/<int:pk>/', toggle_activity_product, name='toggle_activity_product'),
    path('products/error/', error, name='error'),

    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/toggle/<int:pk>/', toggle_activity_category, name='toggle_activity_category'),

    path('versions/', VersionsListView.as_view(), name='versions'),
    path('versions/draft/', VersionsDraftListView.as_view(), name='versions_draft'),
    path('version/<int:pk>/', VersionDetailView.as_view(), name='version'),
    # path('version/create/', VersionCreateView.as_view(), name='version_create'),
    path('version/update/<int:pk>/', VersionUpdateView.as_view(), name='version_update'),
    path('version/delete/<int:pk>/', VersionDeleteView.as_view(), name='version_delete'),
    path('version/toggle/<int:pk>/', Toggle_Activity_Version.as_view(), name='toggle_activity_version'),

    # path('index/', index, name='index'),
    # path('about/', about, name='about'),
    # path('gallery/', gallery, name='gallery'),
    # path('contact/', contact, name='contact'),
]
