from django.http import HttpRequest
from django.shortcuts import render
from products.models import Category, Products
import random

# Create your views here.
def menu_items():
    # menu = [{'title': "О нас", 'products.url_name': 'about'},
    #         {'title': "Домой", 'products.url_name': 'index'},
    #         {'title': "Наши товары", 'products.url_name': 'products'},
    #         {'title': "Галеря", 'products.url_name': 'gallery'},
    #         {'title': "Контакты", 'products.url_name': 'contact'},
    #         ]
    menu = [
        {'title': "О нас" },
        {'title': "Домой"},
        {'title': "Наши товары"},
        {'title': "Галеря"},
        {'title': "Контакты"}
    ]
    return menu
def products(request):
    title = 'Наши товары'
    text = "Интернет-магазин саженцев и семян"
    objects = Products.objects.all().order_by('-id')

    menu = menu_items()
    return render(request, 'products/products.html', {'menu': menu, 'title': title, 'text':text, 'objects':objects,})

def index(request):
    number = 5
    objects = Products.objects.all().order_by('-id')[:5]
    title = 'Последние 5 товаров'
    menu = menu_items()
    return render(request, 'products/index.html', {'menu': menu, 'title': title, 'objects':objects, })

def contact(request):
    title = 'Контакты'
    text = 'Контакты'
    menu = menu_items()
    return render(request, 'products/contact.html', {'menu': menu, 'title': title , 'text': text})
def gallery(request):
    title = 'Галерея'
    text = 'Галерея'
    menu = menu_items()
    objects = Products.objects.all().order_by('-id')
    random_object = random.choice(objects)
    return render(request, 'products/gallery.html', {'menu': menu, 'title': title , 'text': text, 'object': random_object,})
def about(request):
    title = 'О нас'
    text = 'О нас'
    menu = menu_items()
    return render(request, 'products/about.html', {'menu': menu, 'title': title, 'text': text})


