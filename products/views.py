from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django import forms

from products.forms import VersionForm, ProductsForm, CategoryForm
from products.models import Category, Products, Version
import random


# Create your views here.

class GetContact(View):
    def get(self, request):
        title = 'Контакты'
        text = 'Посетить нас:'
        return render(request, 'products/contact.html', {'title': title, 'text': text})

# Version
class VersionsListView(generic.ListView):
    model = Version
    extra_context = {
        'title': 'Версии товаров',
        'text': "Версии товаров"
    }
    # def get_queryset(self, **kwargs):
        # queryset = super().get_queryset()
        # queryset = queryset.filter(is_active=True).order_by('product', 'version_number', 'version_title')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = Version.objects.filter(is_active=True).order_by('product', 'version_number', 'version_title')
        context['products'] = Products.objects.all()
        return context

class VersionsDraftListView(generic.ListView):
    model = Version
    extra_context = {
        'title': 'Неактивные версии',
        'text': 'Неактивные версии'
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_active=False).order_by('product', 'version_number', 'version_title')
    #     return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = Version.objects.filter(is_active=False).order_by('product', 'version_number', 'version_title')
        context['products'] = Products.objects.all()
        return context

class VersionDetailView(generic.DetailView):
    model = Version
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        # contex_data['title'] = contex_data['object']
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        contex_data['product_pk'] = self.object.product.pk
        return contex_data

class VersionCreateView(generic.CreateView):
    model = Version
    form_class = VersionForm
    # fields = ('product', 'version_number', 'version_title', 'is_active')
    success_url = reverse_lazy('products:versions')



class VersionUpdateView(generic.UpdateView):
    model = Version
    form_class = VersionForm
    # fields = ('product', 'version_number', 'version_title', 'is_active')
    success_url = reverse_lazy('products:versions')

class VersionDeleteView(generic.DeleteView):
    model = Version
    success_url = reverse_lazy('products:versions')

class Toggle_Activity_Version(View):
    def get(request, *args, pk, **kwargs):
        text = ""
        version = get_object_or_404(Version, pk=pk)
        if version.is_active:
            version.is_active = False
        else:
            version.is_active = True
        version.save()
        return redirect(reverse('products:version', args=[version.pk]))


class ProductDetailView(generic.DetailView):
    model = Products
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        contex_data['versions'] = Version.objects.filter(product=self.object, is_active=True)
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
    form_class = ProductsForm
    # fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image')
    success_url = reverse_lazy('products:products')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(ProductsCreateView, self).save(*args, **kwargs)


class ProductsUpdateView(generic.UpdateView):
    model = Products
    form_class = ProductsForm
    # fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image')
    success_url = reverse_lazy('products:products')

class ProductsDeleteView(generic.DeleteView):
    model = Products
    success_url = reverse_lazy('products:products')

def toggle_activity_product(request, pk):
    products = get_object_or_404(Products, pk=pk)
    if products.is_active:
        products.is_active = False
    else:
        products.is_active = True
    products.save()
    return redirect(reverse('products:product', args=[products.pk]))

def toggle_activity_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if category.is_active:
        category.is_active = False
    else:
        category.is_active = True
    category.save()
    return redirect(reverse('products:category', args=[category.pk]))



class CategoryDetailView(generic.DetailView):
    model = Category
    # fields = ('name', 'description')
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    # fields = ('name', 'description')
    success_url = reverse_lazy('products:categories')
    # def get_context_data(self, **kwargs):
    #     contex_data = super().get_context_data(**kwargs)
    #     contex_data['title'] = "Изменение категории" + str(self.get_object())
    #     contex_data['text'] = "Изменение категории" + str(self.get_object())
    #     return contex_data

class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    # fields = ('name', 'description')
    success_url = reverse_lazy('products:categories')


class CategoriesListView(generic.ListView):
    model = Category
    extra_context = {
        'title': 'Категории',
        'text': 'Категории'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(is_active=True)
        return queryset

class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = reverse_lazy('products:products')

class GetAbout(View):
    def get(self, request):
        title = 'О нас'
        text = 'Интернет-магазин цветов и саженцев'
        return render(request, 'products/about.html', {'title': title, 'text': text})

class GetIndex(View):
    def get(self, request):
        number = 5
        object_list = Products.objects.all().order_by('-id')[:number]
        title = 'Последние 5 товаров'
        text = 'Последние 5 товаров'
        return render(request, 'products/products_list.html', {
            'title': title,
            'text': text,
            'object_list': object_list,
        })

class GetGallery(View):
    def get(self, request):
        title = 'Галерея'
        text = 'Галерея'
        objects = Products.objects.all().order_by('-id')
        random_object = random.choice(objects)
        return render(request, 'products/products_detail.html',
                      {'title': title, 'text': text, 'object': random_object, })


# def contact(request):
#     title = 'Контакты'
#     text = 'Посетить нас:'
#     return render(request, 'products/contact.html', {'title': title, 'text': text})

# def product(request, pk):
#     title = 'Товар'
#     text = 'Товар'
#     object = Products.objects.get(pk=pk)
#     return render(request, 'products/products_detail.html', {'title': title , 'text': text, 'object': object,})

# def about(request):
#     title = 'О нас'
#     text = 'Интернет-магазин цветов и саженцев'
#     return render(request, 'products/about.html', {'title': title, 'text': text})

# def products(request):
#     title = 'Наши товары'
#     text = "Интернет-магазин саженцев и семян"
#     objects = Products.objects.all().order_by('-id')
#
#     return render(request, 'products/products_list.html', {
#         'title': title, 'text': text, 'objects': objects, })

# def gallery(request):
#     title = 'Галерея'
#     text = 'Галерея'
#     objects = Products.objects.all().order_by('-id')
#     random_object = random.choice(objects)
#     return render(request, 'products/products_detail.html', {'title': title, 'text': text, 'object': random_object, })

# def index(request):
#     number = 5
#     object_list = Products.objects.all().order_by('-id')[:number]
#     title = 'Последние 5 товаров'
#     text = 'Последние 5 товаров'
#     return render(request, 'products/products_list.html', {
#         'title': title,
#         'text': text,
#         'object_list': object_list,
#     })
