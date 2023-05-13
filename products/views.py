from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from products.models import Category, Products
import random

from products.services import send_deactivate_email


# Create your views here.

# def products(request):
#     title = 'Наши товары'
#     text = "Интернет-магазин саженцев и семян"
#     objects = Products.objects.all().order_by('-id')
#
#     return render(request, 'products/products_list.html', {
#         'title': title, 'text': text, 'objects': objects, })


def index(request):
    number = 5
    object_list = Products.objects.all().order_by('-id')[:number]
    title = 'Последние 5 товаров'
    text = 'Последние 5 товаров'
    return render(request, 'products/products_list.html', {
        'title': title,
        'text': text,
        'object_list': object_list,
    })


def contact(request):
    title = 'Контакты'
    text = 'Посетить нас:'
    return render(request, 'products/contact.html', {'title': title, 'text': text})


def gallery(request):
    title = 'Галерея'
    text = 'Галерея'
    objects = Products.objects.all().order_by('-id')
    random_object = random.choice(objects)
    return render(request, 'products/products_detail.html', {'title': title, 'text': text, 'object': random_object, })


class ProductDetailView(generic.DetailView):
    model = Products

    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        # contex_data['title'] = contex_data['object']
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data


class ProductsListView(generic.ListView):
    model = Products
    extra_context = {
        'title': 'Наши товары',
        'text': "Интернет-магазин саженцев и семян"
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

class ProductsCreateView(generic.CreateView):
    model = Products
    fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image')
    success_url = reverse_lazy('products:products')

class ProductsUpdateView(generic.UpdateView):
    model = Products
    fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image')
    success_url = reverse_lazy('products:products')

class ProductsDeleteView(generic.DeleteView):
    model = Products
    success_url = reverse_lazy('products:products')

def toggle_activity(request, pk):
    products = get_object_or_404(Products, pk=pk)
    if products.is_active:
        products.is_active = False
        send_deactivate_email(products)
    else:
        products.is_active = True
    products.save()
    return redirect(reverse('products:product', args=[products.pk]))
class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ('name', 'description')

# def product(request, pk):
#     title = 'Товар'
#     text = 'Товар'
#     object = Products.objects.get(pk=pk)
#     return render(request, 'products/products_detail.html', {'title': title , 'text': text, 'object': object,})
def about(request):
    title = 'О нас'
    text = 'Интернет-магазин цветов и саженцев'
    return render(request, 'products/about.html', {'title': title, 'text': text})
