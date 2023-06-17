from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import request, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from config.settings import CACHE_ENABLED
from products.forms import VersionForm, ProductsForm, CategoryForm, ProductsFormCut
from products.models import Category, Products, Version
import random

from django.shortcuts import render
from products.context_file import current_user

# Create your views here.

def get_category_list():
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = f'category_list'  # Создаем ключ для хранения
        category_list = cache.get(key)  # Пытаемся получить данные
        if category_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        category_list = Category.objects.all()
    return category_list


# Возвращаем результат
# return products_list

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
    def get_queryset(self, **kwargs):
        # queryset = super().get_queryset()
        queryset = Version.objects.filter(is_active=True).order_by('product', 'version_number', 'version_title')
        if queryset.exists():
            return queryset
        else:
            return Version.objects.none()
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

    def get_queryset(self, *args, **kwargs):
        qs = super(*args, **kwargs).get_queryset().filter(is_active=True).order_by('product', 'version_number', 'version_title')
        if qs.exists():
            return qs
        else:
            return Version.objects.none()

    # def get_context_data(self, *args, **kwargs):
    #     context = super(*args, **kwargs).get_context_data(**kwargs)
    #     context['products'] = Products.objects.all()
    #     return context

class VersionUpdateView(generic.UpdateView):
    model = Version
    form_class = VersionForm
    # fields = ('product', 'version_number', 'version_title', 'is_active')

    success_url = reverse_lazy('products:versions')
    def get_queryset(self, *args, **kwargs):
        # queryset = super(*args, **kwargs).get_queryset().filter(is_active=True).order_by('product', 'version_number', 'version_title')
        queryset = super(*args, **kwargs).get_queryset().order_by('product', 'version_number', 'version_title')
        if queryset.exists():
            print("queryset= ", queryset)
            return queryset
        else:
            return Version.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        return context

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

class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Products
    permission_required = ["products.view_products"]
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        contex_data['versions'] = Version.objects.filter(product=self.object, is_active=True)
        return contex_data

class ProductsListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Products
    extra_context = {
        'title': 'Наши товары',
        'text': "Интернет-магазин саженцев и семян"
    }
    permission_required = ['products.view_products']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, is_published=True)
        return queryset
class ProductsNotPublishedView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Products
    permission_required = ["products.view_products"]
    extra_context = {
        'title': 'Наши товары',
        'text': "Неопубликованные товары"
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, is_published=False)
        return queryset

class ProductsCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Products
    form_class = ProductsForm
    # fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image')
    permission_required = ["products.add_products"]
    success_url = reverse_lazy('products:products')

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(ProductsCreateView, self).save(*args, **kwargs)

    def form_valid(self, form):
        """Текущий пользователь будет автором созданного продукта"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())
class ProductsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):

    # permission_required = ["products.change_products", "set_published_status", "set_description_status", "set_category_status"]
    model = Products
    # form_class = ProductsForm
    fields = ('name', 'description', 'price', 'category', 'created_data', 'last_changed_data', 'image', 'is_active', 'user', 'is_published')

    template_name = 'products/products_form_with_formset.html'
    success_url = reverse_lazy('products:products')
    permission_required = ["products.change_products"]

    def get_form_class(self, *args, **kwargs):
        if self.request.user.has_perm('products.set_published_status') and\
            self.request.user.has_perm('products.set_description_status') and\
            self.request.user.has_perm('products.set_category_status'):
            class_form = ProductsForm
        else:
            class_form = ProductsFormCut
        return class_form

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect(reverse_lazy('products:error'))
        return super().get(request, args, kwargs)

    # Вариант 2
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.user != self.request.user:
    #         raise Http404("Вы не являетесь владельцем этого товара")
    #
    #     return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Products, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ProductsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Products
    success_url = reverse_lazy('products:products')
    permission_required = ["products.delete_products"]

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
        # Вариант 1
        # queryset = super().get_queryset()
        #Вариант2
        super()
        queryset = get_category_list()
        return queryset

class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = reverse_lazy('products:products')

class GetAbout(View):
    def get(self, request):
        title = 'О нас'
        text = 'Интернет-магазин цветов и саженцев'
        if current_user(request):
            current_user_name = current_user(request)['current_user']
        else:
            current_user_name = None
        return render(request, 'products/about.html', {'title': title, 'text': text, 'current_user_name': current_user_name})

class GetIndex(View):
    def get(self, request):
        number = 5
        if CACHE_ENABLED:
            # Проверяем включенность кеша
            key = f'products_list'  # Создаем ключ для хранения
            products_list = cache.get(key)  # Пытаемся получить данные
            if products_list is None:
                # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
                products_list = Products.objects.all().order_by('-id')[:number]
                cache.set(key, products_list)
        else:
            # Если кеш не был подключен, то просто обращаемся к БД
            products_list = Products.objects.all()
        # Возвращаем результат
        # return products_list
        title = 'Последние 5 товаров'
        text = 'Последние 5 товаров'
        return render(request, 'products/products_list.html', {
                'title': title,
                'text': text,
                'object_list': products_list,
            })

class GetGallery(View):
    def get(self, request):
        title = 'Галерея'
        text = 'Галерея'
        objects = Products.objects.all().order_by('-id')
        random_object = random.choice(objects)
        return render(request, 'products/products_detail.html',
                      {'title': title, 'text': text, 'object': random_object, })


def error(request, title = 'Ошибка', text = 'Ошибка', error_message = 'Вы не являетесь владельцем этого товара'):
    return render(request, 'products/error.html', {'title': title, 'text': text, 'error_message':error_message})


# class GetIndex(View):
#     def get(self, request):
#         number = 5
#         object_list = Products.objects.all().order_by('-id')[:number]
#         title = 'Последние 5 товаров'
#         text = 'Последние 5 товаров'
#         return render(request, 'products/products_list.html', {
#             'title': title,
#             'text': text,
#             'object_list': object_list,
#         })

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
